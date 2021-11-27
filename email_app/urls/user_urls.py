from django.urls import path
from email_app.views import user_views as views

urlpatterns = [
    path('getroute/', views.getRoutes, name='getroute'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('register/', views.registerUser, name='register'),
]
