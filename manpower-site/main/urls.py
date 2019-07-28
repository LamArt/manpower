from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('engine', views.main, name="engine")
]
