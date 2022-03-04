import json
import time
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.user_models import CompanyProfile
from email_app.models.subscribers_models import GetList, CampaignsLogs, Campaigns, We360SubscriberReportData
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


@api_view(['POST'])
def getWe360data(request):
    user = request.user
    data = request.data['data']
    print(len(data))
    try:
        We360SubscriberReportData.objects.all().delete()
        for item in data:
            company_id = item['company_id']
            company_name = item['company_name']
            time_zone = item['time_zone']
            total_users = item['total_users']
            present_users = item['present_users']
            current_productivity = item['current_productivity']
            previous_productivity = item['previous_productivity']
            productivity_difference = item['productivity_diff']
            absent_users = item['absent_users']
            present_percent = item['present_percent']
            absent_percent = item['absent_percent']
            healthy = item['healthy']
            over_worked = item['over_worked']
            under_utilised = item['under_utilised']
            working_time = item['working_time']
            active_time = item['active_time']
            idle_time = item['idle_time']
            break_time = item['break_time']
            mail_to = item['mail_to']
            attendance_csv_url = item['attendance_csv_url']
            we360_report_data_instance = We360SubscriberReportData.objects.create(subscriber_id=company_id,
                                                                                  subscriber_name=company_name,
                                                                                  mail_to=mail_to, time_zone=time_zone,
                                                                                  total_users=total_users,
                                                                                  present_users=present_users,
                                                                                  current_productivity=current_productivity,
                                                                                  previous_productivity=previous_productivity,
                                                                                  productivity_difference=productivity_difference,
                                                                                  absent_users=absent_users, present_percent=present_percent,
                                                                                  absent_percent=absent_percent, healthy=healthy, over_worked=over_worked,
                                                                                  under_utilised=under_utilised, working_time=working_time, active_time=active_time,
                                                                                  idle_time=idle_time, break_time=break_time, attendence_csv_url=attendance_csv_url)
            we360_report_data_instance.save()
        print('fetched data successfully')
        return Response("fetched successfully")
    except ObjectDoesNotExist:
        message = {'detail': 'unsuccessfully'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
