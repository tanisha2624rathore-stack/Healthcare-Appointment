from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    name=models.CharField(max_length=50)
    specialization=models.CharField(max_length=100)
    available=models.BooleanField(default=True)
    hospital_name=models.CharField(max_length=100)
    experience=models.IntegerField()
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    appo_date=models.DateField() 
    appo_time=models.TimeField()
    status=models.CharField(max_length=20,choices=[
           ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
    ],
    default="confirmed"
    )
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.patient} - {self.doctor}"
class Symptoms(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    symptom=models.CharField(max_length=100)
    age=models.IntegerField()

    def __str__(self):
        return f'{self.patient}{self.symptom}'




# Create your models here.
