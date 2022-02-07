import json
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Campaigns
from email_app.models.user_models import CompanyProfile
from email_app.models.subscribers_models import GetList
from email_app.serializers import TemplatesSerializer, GetListSerializers
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from email_app.thread_tasks import EmailThread
import requests


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
                    mail_sending_list.append({"email": subcriber.email,
                                              "name": subcriber.name})
            # unique_send_list = list(set(mail_sending_list))
            unique_send_list = list({v['email']: v for v in mail_sending_list}.values())
            get_template_to_send(request.user, "hi all", "",
                                 settings.DEFAULT_FROM_EMAIL,
                                 unique_send_list, "email/hyber_dashboard.html",
                                 {"user": request.user,
                                  "attendance": [{"name": "kanchan",
                                                  "att": 30},
                                                 {"name": "sarthak",
                                                  "att": 20}
                                                 ]})
            return Response(unique_send_list, status=status.HTTP_200_OK)
        return Response('You do not have sufficient permission!')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view campaign!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# Function to make email message dynamically

def get_template_to_send(user, email_subject, text_content, from_email, to, template_path, ctx):
    print(to)
    for obj in to:
        print(obj)
        html = render_to_string(template_path, {"name": obj['name']})

        email_message = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=from_email,
            to=[obj['email']],
        )
        email_message.attach_alternative(html, "text/html")
        EmailThread(email_message).start()
    return


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def fetch_subscriber_data_by_api_wwe360():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    data = json.loads(response.text)
    print(data)
    GetList.objects.all().delete()
    for item in data:
        title = item['title']
        body = item['body']
        get_list_instance = GetList.objects.create(title=title, body=body)
        get_list_instance.save()
        serializer = GetListSerializers(get_list_instance, many=False)
    print('fetched data successfully')
    return Response("done")


def get_subscriber_context_data(request):
    pass
