from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Subscribers
from email_app.models.user_models import CompanyProfile
from email_app.serializers import SubscribersSerializer
from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSubscriber(request):
    user = request.user
    print('sarthak', user)
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data

    try:
        subscriber = Subscribers.objects.create(
            company=company_obj,
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )

        serializer = SubscribersSerializer(subscriber, many=False)
        return Response(serializer.data)

    except:
        message = {'detail': 'Staff with this email already exists!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubscribers(request):
    user = request.user

    try:
        company_obj = CompanyProfile.objects.get(user=user)
        print("hello", company_obj.company_id)
        subscribers = Subscribers.objects.filter(company_id=company_obj.id)
        serializer = SubscribersSerializer(subscribers, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Something went wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubscriberById(request, pk):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    try:
        subscriber = Subscribers.objects.get(id=pk)
        serializer = SubscribersSerializer(subscriber, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateSubscriber(request, pk):
    try:
        subscriber = Subscribers.objects.get(id=pk)
        data = request.data
        subscriber.name = data['name']
        subscriber.email = data['email']
        subscriber.phone = data['phone']

        subscriber.save()

        serializer = SubscribersSerializer(subscriber, many=False)

        return Response(serializer.data)

    except:
        message = {'detail': 'Please verify the details!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSubscriber(request, pk):
    subscriberForDeletion = Subscribers.objects.get(id=pk)
    subscriberForDeletion.delete()
    return Response('Subscriber was deleted')
