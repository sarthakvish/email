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
    # path('profile/', views.getUserProfile, name="users-profile"),
    path('', views.getUsers, name="users"),
    # path('<str:pk>/', views.getUserById, name="user"),
    # path('update/<str:pk>', views.updateUser, name="user-update"),
    # path('delete/<str:pk>', views.deleteUser, name="user-delete"),
]
