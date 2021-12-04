from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.user_models import StaffUsers, CompanyProfile
from rest_framework import status
from email_app.serializers import UserSerializerWithToken, StaffSerializerWithUser, StaffProfileSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from email_app.utils import account_activation_token
from email_app.thread_tasks import EmailThread
import pandas as pd
from django.conf import settings
import uuid


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createStaffProfile(request):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['unverified_staff_email'],
            email=data['unverified_staff_email'],
            password=make_password(data['password'])
        )
        user.is_active = False
        user.save()
        staff_profile = StaffUsers.objects.create(
            user=user,
            company_id=company_obj,
            unverified_staff_email=data['unverified_staff_email'],
        )
        current_site = get_current_site(request)
        email_body = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }

        link = reverse('activate', kwargs={
            'uidb64': email_body['uid'], 'token': email_body['token']})

        email_subject = 'Activate your account'

        activate_url = 'http://' + current_site.domain + link

        email_message = EmailMessage(
            email_subject,
            'Hi ' + user.first_name + ', Please the link below to activate your account \n' + activate_url,
            settings.EMAIL_HOST_USER,
            ['sarthakvishwakarma6@gmail.com'],
        )
        EmailThread(email_message).start()

        serializer = StaffSerializerWithUser(staff_profile, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Staff with this email already exists!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verificationView(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        if not account_activation_token.check_token(user, token):
            return redirect('login' + '?message=' + 'User already activated')

        if user.is_active:
            return redirect('login')
        user.is_active = True
        print(user.staffusers.staff_status)
        user.staffusers.staff_status = "VERIFIED"
        user.save()
        user.staffusers.save()
        return redirect('login')
    except:
        pass

    return redirect('login')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exportStaffUser(request):
    staff_obj = StaffUsers.objects.all()
    serializer = StaffSerializerWithUser(staff_obj, many=True)
    df = pd.DataFrame(serializer.data)
    print(df)
    df.drop(['created_at', 'updated_at', 'role_status', 'staff_status', 'user', 'company', 'id'],
            axis=1, inplace=True)
    df.to_csv(f"public/static/excel/{uuid.uuid4()}.csv", encoding="UTF-8")
    return Response("done")


# @api_view(['POST'])
# def registerStaffUser(request):
#     data = request.data
#     user = User.objects.create(
#         first_name=data['name'],
#         username=data['email'],
#         email=data['email'],
#         password=make_password(data['password'])
#     )
#     serializer = UserSerializerWithToken(user, many=False)
#     return Response(serializer.data)
#     # try:
#     #     user = User.objects.create(
#     #         first_name=data['name'],
#     #         username=data['email'],
#     #         email=data['email'],
#     #         password=make_password(data['password'])
#     #     )
#     #     user.staffusers.staff_status ="Active"
#     #     user.save()
#     #     serializer = UserSerializerWithToken(user, many=False)
#     #     return Response(serializer.data)
#     # except:
#     #     message = {'detail': 'User with this email is already exists'}
#     #     return Response(message, status=status.HTTP_400_BAD_REQUEST)
