Mini Resume Management API

Built using FastAPI

Python Version:
3.12.10

Setup Instructions:

1. Clone the repository

2. Create virtual environment:
   python -m venv venv

3. Activate virtual environment:
   venv\Scripts\activate

4. Install dependencies:
   pip install -r requirements.txt

Run the application:

uvicorn main:app --reload

API Endpoints:

GET /health
Check API status

POST /upload
Upload candidate details and resume file

GET /candidates
Filter options:
?skill=Python
?experience=2
?graduation_year=2016

GET /candidate/{id}
Get candidate by ID

DELETE /candidate/{id}
Delete candidate
