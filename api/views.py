from django.shortcuts import render, redirect
from src.models import User, Report, Official
from rest_framework import generics
from api.serializers import UserSerializer, ReportSerializer, UserProfileSerializer, UserProfileUpdateSerializer, ReportHistorySerializer
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import requests

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()


class ReportCreate(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfile(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        user = self.request.user.email
        data= User.objects.filter(email=user)
        return (data)


class UserProfileUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    permission_class = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ReportHistorySerializer


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Incorrect login credentails')
    context = {'page': page}
    return render(request,'api/login.html', context)

@login_required(login_url='loginPage')
def dashboard(request):
    user = request.user
    official = Official.objects.get(user=user)
    department = official.department
    area = official.area
    context = {
        'department': department,
        'area': area,
    }
    return render(request,'api/index.html', context)

@login_required(login_url='loginPage')
def reports(request):
    user = request.user
    official = Official.objects.get(user=user)
    department = official.department
    area = official.area
    department = official.department
    reports = Report.objects.filter(category=department).all()
    reportsAffected = []
    for report in reports:
        try:
            latLong = f"{report.latitude}, {report.longitude}"
            api_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latLong}&result_type=administrative_area_level_2&key=AIzaSyAn90sbAUNy2Em2JDA7iAUy4wO18zfclxc"
            response = requests.get(api_url)
            res = response.json()
            result = res['results'][0]['address_components'][0]['long_name']
            if result == area:
                reportsAffected.append(report)
        except:
            pass
    context = {
        'reports': reportsAffected,
        'department': department,
        'area': area,
    }
    return render(request, 'api/reports.html', context)


@login_required(login_url='loginPage')
def reportDetails(request, pk):
    report = Report.objects.get(id=pk)
    context = {
        "report": report
    }
    return render(request, 'api/report_details.html', context)
