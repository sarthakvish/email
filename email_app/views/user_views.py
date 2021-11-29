from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from email_app.serializers import UserSerializerWithToken, CompanyProfileSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User
from email_app.models.user_models import CompanyProfile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return Response(routes)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email is already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCompanyProfile(request):
    user = request.user
    data = request.data

    try:
        company_profile = CompanyProfile.objects.create(
            user=user,
            company_name=data['company_name'],
            gst_details=data['gst_details'],
            address=data['address']

        )
        serializer = CompanyProfileSerializer(company_profile, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Company profile already created!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
