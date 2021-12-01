from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.user_models import StaffUsers, CompanyProfile
from rest_framework import status
from email_app.serializers import UserSerializerWithToken,StaffSerializerWithUser,StaffProfileSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


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
        staff_profile = StaffUsers.objects.create(
            user=user,
            company_id=company_obj,
            unverified_staff_email=data['unverified_staff_email'],
        )

        serializer = StaffSerializerWithUser(staff_profile, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Staff with this email already exists!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


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
