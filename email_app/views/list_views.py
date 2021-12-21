from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import List, Subscribers
from email_app.models.user_models import CompanyProfile
from taggit.models import Tag
from email_app.serializers import ListSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createList(request):
    try:
        user = request.user
        company_obj = CompanyProfile.objects.get(user=user)
        group_name = Group.objects.get(user=user)
        data = request.data
        print('data', data)
        try:
            if group_name.name == 'staffuser':
                message = {'detail': 'You are not allowed to create list'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            list_instance = List.objects.create(
                company=company_obj,
                name=data['name'],
            )
            list_instance.save()
            tag_names = data['tags']
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                print('tag', tag)
                list_instance.tags.add(tag)
                list_instance.save()
            subscriber_list = data['subscriber']
            for subscriber in subscriber_list:
                subscriber = Subscribers.objects.get(name=subscriber)
                print('subscriber')
                list_instance.subscriber.add(subscriber)
            serializer = ListSerializer(list_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            message = {'detail': 'Entered Subscriber does not exists but list has been created without subscribers '}
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            message = {'detail': 'list already created!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        message = {'detail': 'You dont have permission to create list'}
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLists(request):
    user = request.user
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        print("hello", company_obj.company_id)
        lists = List.objects.filter(company_id=company_obj.id)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)
    except:
        message = {'detail': 'You do not have permission to view all lists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getListById(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if List.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            list = List.objects.get(id=pk)
            serializer = ListSerializer(list, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You do not have permission to view this record ')
    except:
        message = {'detail': 'You are not authorized to view list'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateList(request):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data
    pk = data['id']
    if List.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
        list_obj = List.objects.get(id=pk)
        listquery= list_obj.subscriber.all()
        print(listquery)
        list1=[listquery for listquery in listquery]

        print(list1)
        list_obj.name = data['name']
        # list_obj.list_type = data['list_type']
        list_obj.save()
        # tag_names = data['tags']

        serializer = ListSerializer(list_obj, many=False)

        return Response(serializer.data)
        # try:
        #     list_obj = List.objects.get(id=pk)
        #     print(list_obj.subscriber)
        #     list_obj.name = data['name']
        #     list_obj.list_type = data['list_type']
        #     list_obj.save()
        #     # tag_names = data['tags']
        #
        #     serializer = ListSerializer(list_obj, many=False)
        #
        #     return Response(serializer.data)
        #
        # except:
        #     message = {'detail': 'Please verify the details!'}
        #     return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('You do not have permission to update this subscriber record')
