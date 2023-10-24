from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request, 'FrontEnd/index.html')

def login(request):
    return render(request, 'FrontEnd/login.html')

def signup(request):
    return render(request, 'FrontEnd/signup.html')