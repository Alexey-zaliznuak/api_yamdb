import requests

data = {
    'bio': 'some bio',
    'role': 'user',
}

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NjM1MDE1LCJqdGkiOiI4OTM5NmExYjgxNDk0YzY3OGUwZDc0ZjhmYjNhYmIwMCIsInVzZXJfaWQiOjE0fQ.5jtuko-EmzUnxDa5BUq0aM39J-j_jRDzL1tn8f0LGRc'

default_url = 'http://127.0.0.1:8000/api/v1/'
url = 'users/me/'
url = default_url + url

header = {
    'Authorization': f"Bearer {token}"
}

response = requests.patch(url, data=data, headers=header)

print(response.status_code)
print(response.json())
print(response.headers)
