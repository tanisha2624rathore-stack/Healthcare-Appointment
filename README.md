## Healthcare Appointment System API
1 Description

This is a Healthcare Appointment Backend API built using Django REST Framework (DRF) and FastAPI.
The project allows users to register, view doctor information, book appointments, check slot availability, and analyze symptoms.

2 Features
1 User Signup & Login
2 Doctor Information API
3 Appointment Booking System
4 Slot Availability Check (FastAPI)
5 Smart Slot Suggestion if not available
6 Symptom Checker API (FastAPI)
7 High-risk symptom alert (suggests immediate appoi

3 Tech Stack
Python
Django
Django REST Framework (DRF)
FastAPI
JWT Authentication

##API Endpoints
User & Profile
POST /signup/ → Register user

##Doctor
GET /doctors/ → Get doctor information

##Appointment
POST /appointment/ → Book appointme

##Slot Availability (FastAPI)
Checks if selected time slot is available
If not available → suggests next available slot

## Slot Availability (FastAPI)
Checks if selected time slot is available
If not available → suggests next available 

 Example Request
Signup
{
  "username": "tanisha",
  "password": "123456"
}
Appointment Request
{
  "doctor_id": 1,
  "date": "2026-04-25",
  "time": "10:00 AM"
}

POST /login/ → Login user

SQLite / PostgreSQL
