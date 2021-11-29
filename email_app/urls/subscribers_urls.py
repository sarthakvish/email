from django.urls import path
from email_app.views import subscribers_views as views


urlpatterns = [
    path('', views.getSubscribers, name="subscribers"),
]
