import json
import time
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.user_models import CompanyProfile
from email_app.models.subscribers_models import GetList, CampaignsLogs, Campaigns
from email_app.serializers import TemplatesSerializer, GetListSerializers
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from email_app.thread_tasks import EmailThread
import requests
import threading


@api_view(['POST'])
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

            campaign_log = CampaignsLogs(company=company_obj, campaign=campaign, email_count=len(unique_send_list))
            campaign_log.save()

            get_template_to_send(request.user, "hi all", "",
                                 settings.DEFAULT_FROM_EMAIL,
                                 unique_send_list, "email/update_hyper_dahboard.html",
                                 {"user": request.user,
                                  "attendance": [{"name": "kanchan",
                                                  "att": 30},
                                                 {"name": "sarthak",
                                                  "att": 20}
                                                 ]}, campaign_log)
            # # time.sleep(5)
            thread_list = threading.enumerate()
            print('thread list', thread_list)

            return Response(unique_send_list, status=status.HTTP_200_OK)
        return Response('You do not have sufficient permission!')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to start campaign!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# Function to make email message dynamically

def get_template_to_send(user, email_subject, text_content, from_email, to, template_path, ctx, campaign_log):
    for obj in to:
        print("loop starting...")
        print(obj)
        html = render_to_string(template_path, {"name": obj['name']})

        email_message = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=from_email,
            to=[obj['email']],
        )
        email_message.attach_alternative(html, "text/html")
        print('thread going to start after 2 second')
        # time.sleep(2)

        t = EmailThread(email_message, campaign_log)
        t.daemon = True
        t.start()

        # EmailThread(email_message).start()
        # time.sleep(5)

        # Signal thread to finish
        t.stop()

        # # Wait for thread to finish
        # t.join()

        del t
        # print("waiting for 2 second")
        # time.sleep(2)
        # print("waiting over, and moving to next loop element")
    print(threading.active_count())
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
