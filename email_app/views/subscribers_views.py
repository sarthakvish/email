from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Subscribers
from email_app.models.user_models import CompanyProfile
from email_app.serializers import SubscribersSerializer
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSubscriber(request):
    try:
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
            message = {'detail': 'Subscriber already exists!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        message = {'detail': 'You dont have permission to create subscriber'}
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubscribers(request):
    user = request.user

    try:
        company_obj = CompanyProfile.objects.get(user=user)
        subscribers = Subscribers.objects.filter(Q(company_id=company_obj.id) & Q(is_active=True))
        serializer = SubscribersSerializer(subscribers, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'Something went wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getSubscriberById(request):
    user = request.user
    data = request.data
    pk = data['id']
    company_obj = CompanyProfile.objects.get(user=user)
    if Subscribers.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
        try:
            # subscriber = Subscribers.objects.filter(Q(id=pk) & Q(is_active=True))
            subscriber = Subscribers.objects.get(id=pk)
            # serializer = SubscribersSerializer(subscriber, many=True)
            serializer = SubscribersSerializer(subscriber, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User does not exist'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response("you are not allowed to view this subscriber detail")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateSubscriber(request):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data
    pk = data['id']
    if Subscribers.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
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
    return Response('You do not have permission to update this subscriber record')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteSubscriber(request):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data
    pk = data['id']
    if Subscribers.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
        subscriberForDeletion = Subscribers.objects.get(id=pk)
        subscriberForDeletion.delete()
        return Response('Subscriber was deleted')
    return Response("You do not have permission to delete this subscriber")
