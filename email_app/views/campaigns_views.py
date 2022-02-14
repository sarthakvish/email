from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import List, Subscribers, Campaigns, CampaignsLogs
from email_app.models.user_models import CompanyProfile
from taggit.models import Tag
from email_app.serializers import CampaignSerializer, CampaignSerializerWithoutList, CampaignLogsSerializer, CampaignLogSubscribersSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCampaign(request):
    try:
        user = request.user
        company_obj = CompanyProfile.objects.get(user=user)
        group_name = Group.objects.get(user=user)
        data = request.data
        print('data', data)

        try:
            if group_name.name == 'staffuser':
                message = {'detail': 'You are not allowed to create list'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            campaign_instance = Campaigns.objects.create(
                company=company_obj,
                name=data['name'],
                subject=data['subject'],
                from_email=data['from_email']
            )
            campaign_instance.save()
            tag_names = data['tags']
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                print('tag', tag)
                campaign_instance.tags.add(tag)
                campaign_instance.save()
            listofList = data['lists']
            for listname in listofList:
                list_name = List.objects.get(name=listname)
                campaign_instance.list.add(list_name)
            serializer = CampaignSerializer(campaign_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            message = {'detail': 'Entered list does not exists but campaign has been created without lists '}
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            message = {'detail': 'campaign already created!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        message = {'detail': 'You dont have permission to create campaign'}
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCampaigns(request):
    user = request.user
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        campaigns = Campaigns.objects.filter(company_id=company_obj.id)
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        message = {'detail': 'You do not have permission to view all campaign'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getCampaignById(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if Campaigns.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            campaign = Campaigns.objects.get(id=pk)
            serializer = CampaignSerializer(campaign, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You do not have permission to view this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view list'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateCampaign(request):
    user = request.user
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        data = request.data
        pk = data['id']
        print(data)
        if Campaigns.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            campaign_obj = Campaigns.objects.get(id=pk)
            campaign_obj.name = data['name']
            campaign_obj.subject = data['subject']
            campaign_obj.from_email = data['from_email']
            campaign_obj.save()
            listofList = data['lists']
            campaign_obj.list.clear()
            for listname in listofList:
                list_name = List.objects.get(name=listname)
                campaign_obj.list.add(list_name)
            tag_list = data['tags']
            campaign_obj.tags.clear()
            campaign_obj.tags.clear()
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                campaign_obj.tags.add(tag)
                campaign_obj.save()
            serializer = CampaignSerializer(campaign_obj, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You do not have permission to update this campaign record',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to update campaign'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteCampaignById(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if Campaigns.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            campaign = Campaigns.objects.get(id=pk)
            campaign.delete()
            return Response("Campaign has been deleted successfully!", status=status.HTTP_202_ACCEPTED)
        return Response('You do not have permission to delete this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to delete list'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getCampaignLogs(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if Campaigns.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            campaign = Campaigns.objects.get(id=pk)
            campaign_logs = campaign.campaignslogs_set.all()
            serializer = CampaignLogsSerializer(campaign_logs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You do not have permission to view this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view campaign logs'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getCampaignLogSubscribers(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if CampaignsLogs.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            campaign_log = CampaignsLogs.objects.get(id=pk)
            campaign_logs_subscribers = campaign_log.campaignslogsubscriber_set.all()
            serializer = CampaignLogSubscribersSerializer(campaign_logs_subscribers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You do not have permission to view this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view campaign log related subscribers'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
