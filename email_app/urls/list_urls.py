from django.urls import path
from email_app.views import list_views as views

urlpatterns = [
    path('create_list/', views.createList, name='create_list'),
    path('', views.getLists, name="lists"),
    path('getListById/', views.getListById, name="list"),
    path('updateListById/', views.updateList, name="update_list"),
    path('deleteListById/', views.deleteListById, name="delete_list"),
]
