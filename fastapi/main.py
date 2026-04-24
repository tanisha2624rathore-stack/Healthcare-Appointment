from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime ,timedelta,date
import requests
app=FastAPI()

class check_symptoms(BaseModel):
    symptom:str
    appo_date:str

class doctor_slot(BaseModel):
    doctor_id:int
    appo_date:str
    appo_time:str

high_proirity=[
    "chest",
    "breathing",
    "unconscious",
    "stroke",
    "seizure",
    "bleeding"
]
derm_keyword=["rash", "itching", "redness", "allergy"]
cardio_keyword=["chest", "heart", "pain", "breath", "sweating"]
neuro_keyword=[  "headache", "seizure", "dizziness"]

@app.post('/recomdation')
def AI_recom(data:check_symptoms):
    symptoms=data.symptom.lower()
   
    if any(word in symptoms for word in high_proirity):
        return{
             "risk":"high",
            "priority":"emergency",
            "doctor_type":"cordiologist",
            "mesaage":"take today appointment"
        }

    if any(word in symptoms for word in derm_keyword):
        doctor="Dermlogist"
       
    elif any(word in symptoms for word in cardio_keyword):
        doctor="cardiologist"
         
    elif any(word in symptoms for word in neuro_keyword):
             doctor= "Neurologist"
         
    else:
        doctor="gernerl physician"
    return {
            "doctor_type":doctor,
            "priority": "Normal",
            "risk":"Normal"
        }
   
def slots():
  start_time=datetime.strptime('10:00',"%H:%M")
  end_time=datetime.strptime('16:00',"%H:%M")
  duration=timedelta(minutes=30)
  slot=[]
  current_time=start_time
  while current_time <end_time:
    slot.append(current_time.strftime("%H:%M"))
    current_time+=duration
  return slot  

@app.post("/free-slots")
def free_slots(ai_data:dict):
     
     all_slots = slots()

     response_data = requests.get(
        "http://127.0.0.1:8000/get_booked_slots",
        params={
            "doctor":ai_data["doctor"],
            "appo_date":ai_data['appo_date']
        }
    )
  
     print("STATUS:", response_data.status_code)
     print("TEXT:", response_data.text)

     if response_data.status_code == 200:
           try:
                booked_slots = response_data.json()
           except:
              booked_slots = []
     else:
      booked_slots = []

     booked_slots = [str(t)[:5] for t in booked_slots]
     print(booked_slots)
     free_slots = [
        slot for slot in all_slots
        if slot not in booked_slots
    ]
     print(free_slots)
    
     return{
             "date":ai_data["appo_date"],
             "doctor":ai_data["doctor"],
             "slot":free_slots
         }
     
     



