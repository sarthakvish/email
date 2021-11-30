import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('email_app.urls.user_urls')),
    path('api/staff/', include('email_app.urls.staff_urls')),
    path('api/subscribers/', include('email_app.urls.subscribers_urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
