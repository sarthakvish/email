from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Template
from email_app.models.user_models import CompanyProfile
from email_app.serializers import TemplatesSerializer
from bs4 import BeautifulSoup


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTemplateById(request, pk):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)

    try:
        template = Template.objects.get(id=pk)
        serializer = TemplatesSerializer(template, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Template does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTemplateSourceCode(request, pk):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    try:
        template = Template.objects.get(id=pk)
        serializer = TemplatesSerializer(template, many=False)
        print(template.template)
        file = open(f"media/{template.template}", 'r', encoding='utf-8')
        source_code = file.read()
        S = BeautifulSoup(source_code, 'html.parser')
        print(source_code)
        return Response(S.prettify())
    except:
        message = {'detail': 'Template does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
