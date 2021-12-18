from django.urls import path
from email_app.views import staff_views as views

urlpatterns = [
    path('create_staff_profile/', views.createStaffProfile, name='create_staff_profile'),
    path('activate/<uidb64>/<token>',
         views.verificationView, name='activate'),
    path('export_staff/', views.exportStaffUser, name='export_staff'),
    path('', views.getStaff, name="staffs"),
    path('getStaffById/', views.getStaffById, name="staff"),
    path('updateStaffById/', views.updateStaff, name="staff-update"),
    path('deleteStaffById/', views.deleteStaff, name="staff-delete"),

]
