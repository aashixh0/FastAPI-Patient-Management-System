from fastapi import FastAPI ,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated,Optional
import json

class Patient(BaseModel):

    id : Annotated[str , Field(...,description='ID of the Patient',examples=['P001'])]
    name : Annotated[str,  Field(...,description='Name of the Patient',max_length=50)]
    city : Annotated[str,  Field(...,description='City of the Patient',max_length=15)]
    age : Annotated[int,  Field(...,description='Age of the Patient',ge=0,le=120)]
    gender : Annotated[Literal['male','female','others'] , Field(...,description='Gender of the patient')]
    height : Annotated[float , Field(...,description='Height of the patient (in metres)',gt=0)]
    weight : Annotated[float , Field(...,description='Weight of the patient (in kg)',gt=0)]

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

class UpdatePatient(BaseModel):

    name : Annotated[Optional[str],  Field(default=None,description='Name of the Patient',max_length=50)]
    city : Annotated[Optional[str],  Field(default=None,description='City of the Patient',max_length=15)]
    age : Annotated[Optional[int],  Field(default=None,description='Age of the Patient',ge=0,le=120)]
    gender : Annotated[Optional[Literal['male','female','others']] , Field(default=None,description='Gender of the patient')]
    height : Annotated[Optional[float] , Field(default=None,description='Height of the patient (in metres)',gt=0)]
    weight : Annotated[Optional[float] , Field(default=None,description='Weight of the patient (in kg)',gt=0)]


app = FastAPI()

def load_data():
    with open ("patient.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open ('patient.json','w') as f:
        json.dump(data,f)


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
def view_patient(patient_id : str = Path(...,description='The ID of the patient',examples="P001")):
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
    data  = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400 , detail='Patient already exists!!')
    
    # add hte patient as it doesn't exists already
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201,content={'Message' : 'Patient Created Succesfully!!'})

@app.put('/edit/{patient_id}')
def upadate_patient(patient_id: str,patient_update:UpdatePatient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient Not Found!')
    
    existing_patient_info = data[patient_id]

    data_to_be_updated = patient_update.model_dump(exclude_unset=True)

    for key,val in data_to_be_updated.items():
        existing_patient_info[key] = val

    # Now thw exisiting_patient_info contains the updated data
    # Now we have to just insert this update data back into the database
    # but as we have bmi and validate as computed fields so we need to change the value of the omputed field also
    # to do this we can create a pydantic object oof the Patient Model which will get the existing patient info as input ad then calculate the updated computed fields
    existing_patient_info['id'] = patient_id
    final_record = Patient(**existing_patient_info)

    existing_patient_info = final_record.model_dump(exclude=['id'])

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=201,content={'Message' : 'Patient Info Update Successfully!!'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Error : Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient Deleted Successfully'})