from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import List, Subscribers, Campaigns, CampaignsLogs
from email_app.models.user_models import CompanyProfile, StaffUsers
from taggit.models import Tag
from email_app.serializers import CampaignSerializer, CampaignSerializerWithoutList, CampaignLogsSerializer, \
    CampaignLogSubscribersSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDashboardAnalytics(request):
    user = request.user
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        campaigns_count = Campaigns.objects.filter(company_id=company_obj.id).count()
        staff_count = StaffUsers.objects.filter(company_id=company_obj.id).count()
        public_lists_count = List.objects.filter(Q(company_id=company_obj.id) & Q(list_type='PUBLIC')).count()
        private_lists_count = List.objects.filter(Q(company_id=company_obj.id) & Q(list_type='PRIVATE')).count()
        active_subscribers_count = Subscribers.objects.filter(Q(company_id=company_obj.id) & Q(is_active=True)).count()
        inactive_subscribers_count = Subscribers.objects.filter(
            Q(company_id=company_obj.id) & Q(is_active=False)).count()
        context = {
            'campaigns_count': campaigns_count,
            'public_lists_count': public_lists_count,
            'private_lists_count': private_lists_count,
            'active_subscribers_count': active_subscribers_count,
            'inactive_subscribers_count': inactive_subscribers_count,
            'staff_count': staff_count,
        }
        return Response(context)
    except ObjectDoesNotExist:
        message = {'detail': 'You do not have permission to view analytics record'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
