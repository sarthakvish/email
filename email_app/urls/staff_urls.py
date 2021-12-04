from django.urls import path
from email_app.views import staff_views as views

urlpatterns = [
    path('create_staff_profile/', views.createStaffProfile, name='create_staff_profile'),
    path('activate/<uidb64>/<token>',
         views.verificationView, name='activate'),
    # path('register_staff/', views.registerStaffUser, name='register_staff'),
    path('export_staff/', views.exportStaffUser, name='export_staff'),

]
