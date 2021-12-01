from django.urls import path
from email_app.views import staff_views as views

urlpatterns = [
    path('create_staff_profile/', views.createStaffProfile, name='create_staff_profile'),
    # path('register_staff/', views.registerStaffUser, name='register_staff'),

]
