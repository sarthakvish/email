from django.urls import path
from email_app.views import list_views as views

urlpatterns = [
    path('create_list/', views.createList, name='create_list'),
    path('', views.getLists, name="subscribers"),
]
