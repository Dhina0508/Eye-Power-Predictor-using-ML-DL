from django.shortcuts import render
from django.urls import path
from .views import *

# Create your views here.
urlpatterns = [
     path('predict/', PredictPower.as_view(), name='predict'),
     ]