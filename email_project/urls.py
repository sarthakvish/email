import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from email_project import settings
from django_ses.views import SESEventWebhookView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/users/', include('email_app.urls.user_urls')),
                  path('api/staff/', include('email_app.urls.staff_urls')),
                  path('api/subscribers/', include('email_app.urls.subscribers_urls')),
                  path('api/templates/', include('email_app.urls.templates_urls')),
                  path('api/lists/', include('email_app.urls.list_urls')),
                  path('api/campaigns/', include('email_app.urls.campaigns_urls')),
                  path('api/send/', include('email_app.urls.sending_urls')),
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('ses/event-webhook/', SESEventWebhookView.as_view(), name='handle-event-webhook'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
