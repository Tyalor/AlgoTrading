# finance_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page with form
]
