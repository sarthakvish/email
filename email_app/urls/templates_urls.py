from django.urls import path
from email_app.views import templates_views as views

urlpatterns = [
    path('', views.getTemplates, name="templates"),
    path('getTemplateById/', views.getTemplateById, name="template"),
    path('getTemplateSourceCode/', views.getTemplateSourceCode, name="source"),
    path('deleteTemplateById/', views.deleteTemplateById, name="delete-template"),
]
