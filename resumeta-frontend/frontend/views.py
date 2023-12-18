import os

import requests
from django.http import HttpResponse
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("API_URL")

def index(request):
    response = requests.get(f"{API_URL}/resumes/")
    return HttpResponse(response.content)