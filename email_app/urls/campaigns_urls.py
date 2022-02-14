from django.urls import path
from email_app.views import campaigns_views as views

urlpatterns = [
    path('create_campaign/', views.createCampaign, name='create_campaign'),
    path('', views.getCampaigns, name="campaigns"),
    path('getCampaignById/', views.getCampaignById, name="campaign"),
    path('updateCampaignById/', views.updateCampaign, name="update_campaign"),
    path('deleteCampaignById/', views.deleteCampaignById, name="delete_campaign"),
    path('getCampaignLogs/', views.getCampaignLogs, name="campaign_logs"),
    path('getCampaignLogSubscribers/', views.getCampaignLogSubscribers, name="campaign_log_subscribers"),
]
