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
                subscriber = Subscribers.objects.get(name=subscriber, company=company_obj)
                print('subscriber')
                list_instance.subscriber.add(subscriber)
            serializer = ListSerializer(list_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            message = {'detail': 'Entered Subscriber does not exists but list has been created without subscribers '}
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            message = {'detail': 'list already created, please select another name for new list!'}
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
    except ObjectDoesNotExist:
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
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to view list'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateList(request):
    user = request.user
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        data = request.data
        pk = data['id']
        if List.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            list_obj = List.objects.get(id=pk)
            list_obj.name = data['name']
            list_obj.list_type = data['list_type']
            list_obj.save()
            subscriber_list = data['subscriber']
            list_obj.subscriber.clear()
            for subscriber in subscriber_list:
                subscriber = Subscribers.objects.get(name=subscriber, company=company_obj)
                print('subscriber')
                list_obj.subscriber.add(subscriber)
            tag_list = data['tags']
            list_obj.tags.clear()
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                print('tag', tag)
                list_obj.tags.add(tag)
                list_obj.save()
            serializer = ListSerializer(list_obj, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You do not have permission to update this list record',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to update list'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteListById(request):
    user = request.user
    data = request.data
    pk = data['id']
    try:
        company_obj = CompanyProfile.objects.get(user=user)
        if List.objects.filter(Q(id=pk) & Q(company=company_obj)).exists():
            list = List.objects.get(id=pk)
            list.delete()
            return Response("list has been deleted successfully!", status=status.HTTP_202_ACCEPTED)
        return Response('You do not have permission to delete this record ')
    except ObjectDoesNotExist:
        message = {'detail': 'You are not authorized to delete list'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


