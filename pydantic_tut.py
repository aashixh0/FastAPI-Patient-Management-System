from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

    name:Annotated[str, Field(description="Patient's name",max_length=50)]
    age:Annotated[int, Field(description="Patient's age",gt=0,le=120)]
    email:EmailStr
    profile:AnyUrl
    bmi: float
    married: Annotated[bool, Field(default=None,description='Is Patient Married?')]
    allergies: Optional[List[str]] = None
    contact: dict[str,str]

def insert(patient : Patient):

    print(patient.name)
    print(patient.age)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)

patient_info = {'name':'aashish','age':22,'bmi':25,'married':False,'allergies':['dust','pollen'],'contact':{'phone':'1234567890','email':'aashish@example.com'}}

new_patient = Patient(**patient_info)
insert(new_patient)