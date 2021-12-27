from django.urls import path
from email_app.views import sending_views as views

urlpatterns = [
    path('campaign_subscriber/', views.getCampaignsSubscriber, name='campaign_subscriber'),
]