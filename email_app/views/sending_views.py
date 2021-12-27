from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Campaigns
from email_app.models.user_models import CompanyProfile
from email_app.serializers import TemplatesSerializer
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist


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
            return Response(unique_send_list, status=status.HTTP_200_OK)
        return Response('You do not have permission to view this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view campaign'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
