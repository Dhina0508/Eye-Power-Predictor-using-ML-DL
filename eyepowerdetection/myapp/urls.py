from django.shortcuts import render
from django.urls import path
from .views import PredictPower,diagonisis

# Create your views here.
urlpatterns = [
     path('power/', PredictPower.as_view(), name='power'),
     path('predict/', diagonisis.as_view(), name='predict'),
     ]