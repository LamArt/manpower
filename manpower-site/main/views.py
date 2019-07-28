from django.contrib.sessions.backends import db
from django.shortcuts import render
from django.http import HttpResponse

from extractvacancy.models import Vacancy


def main(request):
    #CHANGE THE CONTEXT VALUE TO CHANGE THE DATABASE OUTPUT
    context = Vacancy.objects.all()
    return render(request, 'manpower-site/home.html', {"context": context})


def login(request):
    return render(request, 'manpower-site/login-landing.html')
