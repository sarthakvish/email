from django.urls import path
from email_app.views import user_views as views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('getroute/', views.getRoutes, name='getroute'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register/', views.registerUser, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_company_profile/', views.createCompanyProfile, name='create_company_profile'),
    path('get_company_profile/', views.getCompanyProfile, name='get_company_profile'),
    path('update_company_profile/', views.updateCompanyProfile, name='update_company_profile'),
    path('profile/', views.getUserProfile, name="users-profile"),
    path('', views.getUsers, name="users"),
    path('getUserById/', views.getUserById, name="user"),
    path('updateUserById/', views.updateUser, name="user-update"),
    path('deleteUserById/', views.deleteUser, name="user-delete"),
]
