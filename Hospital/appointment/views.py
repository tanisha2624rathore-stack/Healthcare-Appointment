from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from  django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Doctor,Appointment
from .serializers import DoctorSerializer,AppointmentSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
import requests

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    username=request.data.get('username')
    password=request.data.get('password')
  
    if User.objects.filter(username=username).exists():
        return Response({'error':'Username already exists'},status=400)
    user=User.objects.create_user(username=username,password=password)
    refresh=RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    })
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')

    user=authenticate(request,username=username,password=password)
    if user is not None:
       refresh=RefreshToken.for_user(user)
       return Response({
        "message":"logging successfully",
        "refresh":str(refresh),
        "access":str(refresh.access_token)
    })
    return Response({'error':' not authenticate'},status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_doctor(request):
    print(request.user)
    print(request.user.is_authenticated)
    doctor_list=Doctor.objects.filter(available=True).all()
    serializer=DoctorSerializer(doctor_list,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):

    doctor_id = request.data.get('doctor_id')
    date = request.data.get('appo_date')
    time = request.data.get('appo_time')
  
    response=requests.post(
        url="http://127.0.0.1:8001/free-slots",
        json={
            "appo_date":date,
            "doctor":doctor_id
           
        }
    )
    response_data=response.json()

    available_slots = response_data.get("slot", [])
    if time not in available_slots:
        return Response(
            {"error":"Selected slot is not available",
             "available_slots": available_slots},
            status=400
        )

    Appointment.objects.create(
        patient=request.user,
        doctor_id=doctor_id,
        appo_date=date,
        appo_time=time,
        
    )
    return Response({
        "message": "Appointment Booked",
        "available_slots": available_slots

    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_appointment(request):
    show_data=Appointment.objects.all()
    serializer=AppointmentSerializer(show_data,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_booked_slots(request):
    doctor_id = request.query_params.get("doctor")
    appo_date = request.query_params.get("appo_date")

    booked = Appointment.objects.filter(
        doctor_id=doctor_id,
        appo_date=appo_date,
        status="pending"
    ).values_list("appo_time", flat=True)

    return Response(list(booked)) 

@api_view(["POST"])
def symptom_view(request):
    symptoms=request.data.get('symptoms')
    age=request.data.get('age')
    if not symptoms:
        return Response(
            {"error": "symptom and  required"},
            status=400
        )

    response = requests.post(
        "http://127.0.0.1:8001/recomdation",
        json={
            "symptom": symptoms,
           
        }
    )
    response_data=response.json()
    return Response({
        "message": "Symptom analyzed successfully",
        "data": response_data
    })


    

# Create your views here.
