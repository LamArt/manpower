from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(request):
    return render(request, 'manpower-site/home.html')

def login(request):
    return render(request, 'manpower-site/login-landing.html')