from django.urls import path, include, re_path
from knox import views as knox_views
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api-history', views.ReportViewSet)

urlpatterns = [
    path('api-register/', views.UserCreate.as_view()),
    path('api-login/', views.LoginAPI.as_view(), name='login'),
    path('api-logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api-logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api-report/', views.ReportCreate.as_view()),
    path('api-contactCreate/', views.ContactCreate.as_view()),
    path('api-userprofile/', views.UserProfile.as_view()),
    path('api-contactView/', views.ContactView.as_view()),
    path('api-userprofileupdate/<int:pk>/', views.UserProfileUpdate.as_view()),
    path('api-notificationsView/', views.NotificationView.as_view()),
    path('api-notificationsCreate/', views.NotificationCreate.as_view()),
    path('api-safeTripCreate/', views.SafeTripCreate.as_view()),
    path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('reports/', views.reports, name='reports'),
    path('reportDetails/<str:pk>/', views.reportDetails, name='reportDetails'),

]
