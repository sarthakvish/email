from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import email_app.models.user_models
from email_app.serializers import UserSerializerWithToken, CompanyProfileSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User
from email_app.models.user_models import CompanyProfile
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib.auth.models import Permission

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def getUserById(request):
    data = request.data
    pk = data['id']
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


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
        group = Group.objects.get(name='company_admin')
        print('group', group)
        user.groups.add(group)
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except IntegrityError as e:
        message = {'detail': 'User with this email is already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCompanyProfile(request):
    user = request.user
    data = request.data
    group_name = Group.objects.get(user=user)
    # permissions = Permission.objects.get(user=user.id)
    # print('permission', permissions)
    # if user.has_perm('email_app.company_profile.can_add_company_profile'):
    #     print("yes has permission")

    try:
        if group_name.name == 'staffuser':
            message = {'detail': 'You are not allowed to create company!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            company_profile = CompanyProfile.objects.create(
                user=user,
                company_name=data['company_name'],
                gst_details=data['gst_details'],
                address=data['address']

            )
            serializer = CompanyProfileSerializer(company_profile, many=False)
            return Response(serializer.data)
    except IntegrityError as e:
        message = {'detail': 'Company profile already created!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    data = request.data
    pk = data['id']
    try:
        user = User.objects.get(id=pk)
        data = request.data
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.is_staff = data['isAdmin']

        user.save()

        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)

    except:
        message = {'detail': 'Please verify the details!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def deleteUser(request):
    data = request.data
    pk = data['id']
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')

