from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Template
from email_app.models.user_models import CompanyProfile
from email_app.serializers import TemplatesSerializer
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTemplates(request):
    user = request.user
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        templates = Template.objects.filter(company_id=company_obj.id)
        serializer = TemplatesSerializer(templates, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Something went wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getTemplateById(request):
    user = request.user
    data = request.data
    pk = data['id']

    try:
        company_obj = CompanyProfile.objects.get(user=user)
        template = Template.objects.get(id=pk)
        serializer = TemplatesSerializer(template, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Template does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getTemplateSourceCode(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if Template.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            template = Template.objects.get(id=pk)
            serializer = TemplatesSerializer(template, many=False)
            print(template.template)
            file = open(f"templates/{template.template}", 'r', encoding='utf-8')
            source_code = file.read()
            S = BeautifulSoup(source_code, 'html.parser')
            print(source_code)
            context = {
                'data': serializer.data,
                'source': S.prettify(),
            }
            return Response(context)
        return Response("You do not have permission to view this template source!")
    except ObjectDoesNotExist:
        message = {'detail': 'Template does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteTemplateById(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if Template.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            template = Template.objects.get(id=pk)
            template.delete()
            return Response("Template has been deleted successfully!", status=status.HTTP_202_ACCEPTED)
        return Response('You do not have permission to delete this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to delete Template'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
