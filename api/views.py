from django.shortcuts import render, redirect
from src.models import User, Report, Official, Notification, Contact, SafeTripReport
from rest_framework import generics
from api.serializers import (
    RegisterSerializer, 
    ReportSerializer, 
    UserProfileSerializer, 
    UserProfileUpdateSerializer, 
    ReportHistorySerializer, 
    NotificationViewSerializer, 
    NotificationCreateSerializer,
    ContactCreateSerializer,
    ContactViewSerializer,
    SafeTripCreateSerializer,
)
from rest_framework import permissions, generics
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
from knox.models import AuthToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class UserCreate(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserProfileSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ReportCreate(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class ContactCreate(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactView(generics.ListAPIView):
    serializer_class = ContactViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Contact.objects.all()
        user = self.request.user.id
        data= Contact.objects.filter(user=user)
        return (data)

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



class NotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state', 'lga']




class NotificationCreate(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class SafeTripCreate(generics.CreateAPIView):
    queryset = SafeTripReport.objects.all()
    serializer_class = SafeTripCreateSerializer
    permission_classes = [permissions.IsAuthenticated]







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


