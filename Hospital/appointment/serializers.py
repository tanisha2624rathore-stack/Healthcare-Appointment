from rest_framework.serializers import ModelSerializer
from .models import Doctor,Appointment,Symptoms
from rest_framework import serializers

class DoctorSerializer(ModelSerializer):
    
     class Meta:
        model=Doctor
        fields = "__all__"


class AppointmentSerializer(ModelSerializer):
   
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True
    )

    doctor_name = serializers.CharField(
        source="doctor.name",
        read_only=True
    )

    patient_name = serializers.CharField(
        source='patient.username',
        read_only=True
    )
    class Meta:
        model=Appointment
        fields=['id','appo_date','appo_time','status','doctor_name','patient_name','doctor']
class SymptomSerilaizer(ModelSerializer):
    class Meta:
        model=Symptoms
        fields="__all__"