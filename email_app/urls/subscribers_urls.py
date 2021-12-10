from django.urls import path
from email_app.views import subscribers_views as views

urlpatterns = [
    path('create_subscriber/', views.createSubscriber, name='create_subscriber'),
    path('', views.getSubscribers, name="subscribers"),
    path('<str:pk>/', views.getSubscriberById, name="staff"),
    path('update/<str:pk>', views.updateSubscriber, name="subscriber-update"),
    path('delete/<str:pk>', views.deleteSubscriber, name="subscriber-delete"),
]
