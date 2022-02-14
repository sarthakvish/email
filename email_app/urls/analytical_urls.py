from django.urls import path
from email_app.views import analytical_views as views

urlpatterns = [
    path('getDashboardAnalytics/', views.getDashboardAnalytics, name="dashboard_analytics"),
]
