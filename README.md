# YaMDb API
### Describe
Api for YaMDb

created by
[redoc documentation](/api_yamdb/static/redoc.yaml)

### Technology
Python 3.9

Django 3.2

DRF 3.12.4

PyJWT 2.1.0

drf-yasg 1.21.5

SQLite

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

### Start in dev mode
- Create environment
    
Linux/MacOS:
```
python3 -m venv env
```
Windows:
```
python -m venv env
```
- Install dependencies from requirements.txt
```
pip install -r requirements.txt
```
- In the folder with manage.py run next command:
```
python manage.py runserver
```
