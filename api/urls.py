from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api-history', views.ReportViewSet)

urlpatterns = [
    path('api-register', views.UserCreate.as_view()),
    path('api-report', views.ReportCreate.as_view()),
    path('api-userprofile/', views.UserProfile.as_view()),
    path('api-userprofileupdate/<int:pk>/', views.UserProfileUpdate.as_view()),
    path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('reports/', views.reports, name='reports'),
    path('reportDetails/<str:pk>/', views.reportDetails, name='reportDetails'),

]