from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


def home(request):
    return HttpResponse("hello")