from django import forms

from extractvacancy.models import Vacancy


class CategoryForm(forms.Form):
    category_name = forms.ModelChoiceField(label=u'Минипрофессия', queryset=Vacancy.objects.values('name').distinct())
    # заменить name на category_name
