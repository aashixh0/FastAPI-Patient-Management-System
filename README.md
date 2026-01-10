# 🏥 Patient Management System API

A FastAPI-based Patient Management System that enables efficient storage, retrieval, updating, deletion, and sorting of patient medical records.
This API is designed to simplify handling patient information and includes automatic BMI computation and health status evaluation.

## 📌 Features

- Create new patient records
- Retrieve all patients or specific patient details
- Update patient information partially or fully
- Delete patient records
- Sort patients by medical attributes
- Automatically computes:
  - BMI
  - Health Status (Underweight | Normal | Overweight | Obese) using computed fields

## 🛠️ Tech Stack

- Python
- FastAPI
- Pydantic (Validation & Computed Fields)
- JSON File Storage
- Uvicorn (Server)

## 🚀 API Documentation

FastAPI provides auto-generated docs at:

**Swagger UI:** http://127.0.0.1:8000/docs

## 📝 Request Body Example

```json
{
  "id": "P001",
  "name": "John Doe",
  "city": "Delhi",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
```

## 🔧 Setup

```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Run

```bash
uvicorn main:app --reload
```
