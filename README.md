# UBS Currency Exchange API (FastAPI Backend)

This is a backend API for managing and viewing currency exchange rates using FastAPI and PostgreSQL. Built for the UBS assessment project.

## 🔧 Features

- Fetches exchange rates from the U.S. Treasury API and stores them in PostgreSQL
- API to get all exchange rates with optional threshold filtering
- POST endpoint to add new entries
- CORS enabled for frontend communication
- Auto-sync logic built in (manual trigger)

## 🏗 Project Structure

main.py - FastAPI app and routes
database.py - SQLAlchemy DB config
models.py - DB models
schemas.py - Pydantic schemas
crud.py - DB logic (create, read)
render.yaml - Deployment config
requirements.txt - Python dependencies


##  Run Locally

### 1. Clone the Repo

```bash
git clone 
cd ubs-fastapi-backend

pip install -r requirements.txt

uvicorn main:app --reload


GET /api/conversions - Get all exchange records

POST /api/conversions - Add a new record

GET / - Health check