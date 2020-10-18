from django import forms
from django.forms import fields
from django.shortcuts import render
from django.http import HttpResponse

from extractvacancy.models import Vacancy
from main.forms import CategoryForm


def main(request):
    form = CategoryForm()
    return render(request, 'manpower-site/home.html', {'category_names_form': form})

def login(request):
    return render(request, 'manpower-site/login-landing.html')