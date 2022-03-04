from django.urls import path
from email_app.views import sending_views as views

urlpatterns = [
    path('campaign_subscriber/', views.getCampaignsSubscriber, name='campaign_subscriber'),
    # path('fetch_data_from_we360/', views.fetch_subscriber_data_by_api_wwe360, name='fetch_data_we360'),
    path('getwe360data/', views.getWe360data, name='getwe360data'),
]
