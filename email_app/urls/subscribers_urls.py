from django.urls import path
from email_app.views import subscribers_views as views

urlpatterns = [
    path('create_subscriber/', views.createSubscriber, name='create_subscriber'),
    path('', views.getSubscribers, name="subscribers"),
    path('getSubscriberById/', views.getSubscriberById, name="staff"),
    path('updateSubscriberById/', views.updateSubscriber, name="subscriber-update"),
    path('deleteSubscriberById/', views.deleteSubscriber, name="subscriber-delete"),
]
