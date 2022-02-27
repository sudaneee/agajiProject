from django.urls import path, include, re_path
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api-history', views.ReportViewSet)

urlpatterns = [
    path('api-register', views.UserCreate.as_view()),
    path('api-report', views.ReportCreate.as_view()),
    path('api-contactCreate', views.ContactCreate.as_view()),
    path('api-userprofile/', views.UserProfile.as_view()),
    path('api-contactView/', views.ContactView.as_view()),
    path('api-userprofileupdate/<int:pk>/', views.UserProfileUpdate.as_view()),
    path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('reports/', views.reports, name='reports'),
    path('api-notificationsView/', views.NotificationView.as_view()),
    path('api-notificationsCreate/', views.NotificationCreate.as_view()),
    path('reportDetails/<str:pk>/', views.reportDetails, name='reportDetails'),

]