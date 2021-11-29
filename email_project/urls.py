
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('email_app.urls.user_urls')),
    path('api/subscribers/', include('email_app.urls.subscribers_urls')),
]
