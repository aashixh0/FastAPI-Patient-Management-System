from fastapi import FastAPI ,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
import json

class Patient(BaseModel):

    id : Annotated[str , Field(...,description='ID of the Patient',examples=['P001'])]
    name : Annotated[str,  Field(...,description='Name of the Patient',max_length=50)]
    city : Annotated[str,  Field(...,description='City of the Patient',max_length=15)]
    age : Annotated[int,  Field(...,description='Age of the Patient',ge=0,le=120)]
    gender : Annotated[Literal['male','female','others'] , Field(description='Gender of the patient')]
    height : Annotated[float , Field(...,description='Height of the patient (in metres)')]
    weight : Annotated[float , Field(...,description='Weight of the patient (in kg)')]

    @computed_field
    @property
    def bmi(self)-> float:
        return self.weight/self.height**2
    
    @computed_field
    @property
    def validate(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi <30:
            return 'Overweight'
        return 'Obese'


app = FastAPI()

def load_data():
    with open ("patient.json","r") as f:
        data = json.load(f)
    return data

@app.get('/')
def home():
    return "WELCOME TO PATIENT MANAGEMENT DASHBOARD"

@app.get("/about")
def about():
    return {'message' : 'This is an API for patient management system build to manage the details of patient in an efiicient way to solve the burden of maintaining records and displaying them manually'}

@app.get("/patient")
def view():
    data =  load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(...,description='The ID of the patient',example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patient(sort_by:str = Query(...,description='Sort Data on the basis of features like age,height,weight,bmi'),order:str = Query(default='asc',description='Sort Data in Ascending or Descending')):
    valid_sort_fields = ['age','height','weight','bmi']
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400,detail=f'Invalid Sorting Column. Select from {valid_sort_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404,detail='Invalid Order by value. Select from "asc" or "desc"')
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == 'desc'))
    return sorted_data

@app.post('/create')
def add_patient(patient : Patient):

    if patient.id in