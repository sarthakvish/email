from django.urls import path
from email_app.views import templates_views as views

urlpatterns = [
    path('', views.getTemplates, name="templates"),
    path('<str:pk>/', views.getTemplateById, name="template"),
    path('source/<str:pk>/', views.getTemplateSourceCode, name="source"),
]
