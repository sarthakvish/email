from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Campaigns
from email_app.models.user_models import CompanyProfile
from email_app.serializers import TemplatesSerializer
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from email_app.thread_tasks import EmailThread


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCampaignsSubscriber(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if Campaigns.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            campaign = Campaigns.objects.get(id=pk)
            campaign_lists = campaign.list.all()
            mail_sending_list = []

            for list_obj in campaign_lists:
                subscribers = list_obj.subscriber.all()
                for subcriber in subscribers:
                    mail_sending_list.append(subcriber.email)
            unique_send_list = list(set(mail_sending_list))
            print(unique_send_list)
            get_template_to_send(request.user, "hi all", "",
                                 settings.DEFAULT_FROM_EMAIL,
                                 unique_send_list, "email/hyber_dashboard.html", {"user": request.user})
            return Response(unique_send_list, status=status.HTTP_200_OK)
        return Response('You do not have permission to view this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view campaign'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# Function to make email message dynamically

def get_template_to_send(user, email_subject, text_content, from_email, to, template_path, ctx):
    html = render_to_string(template_path, {"user": ctx})

    email_message = EmailMultiAlternatives(
        subject=email_subject,
        body=text_content,
        from_email=from_email,
        bcc=to,
    )
    email_message.attach_alternative(html, "text/html")
    EmailThread(email_message).start()
    return email_message
