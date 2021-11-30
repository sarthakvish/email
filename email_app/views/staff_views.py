from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.user_models import StaffUsers, CompanyProfile
from email_app.serializers import StaffProfileSerializer
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createStaffProfile(request):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    company_id = company_obj.company_id
    data = request.data
    company_profile = StaffUsers.objects.create(
        user=user,
        company_id=company_obj,
        name=data['name'],
        email=data['email'],

    )
    serializer = StaffProfileSerializer(company_profile, many=False)
    return Response(serializer.data)

    # try:
    #     company_profile = StaffUsers.objects.create(
    #         user=user,
    #         company_id=company_id,
    #         name=data['name'],
    #         email=data['email'],
    #
    #     )
    #     serializer = StaffProfileSerializer(company_profile, many=False)
    #     return Response(serializer.data)
    # except:
    #     message = {'detail': 'Staff with this email already exists!'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)
