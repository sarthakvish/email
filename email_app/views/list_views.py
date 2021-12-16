from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import List, Subscribers
from email_app.models.user_models import CompanyProfile
from taggit.models import Tag
from email_app.serializers import ListSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createList(request):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data
    print('data', data)

    try:
        list_instance = List.objects.create(
            company=company_obj,
            name=data['name'],
        )
        list_instance.save()
        tag_names = data['tags']
        print("tagname", tag_names)
        print("type")
        print(type(tag_names))
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
        return Response(serializer.data)

    except:
        message = {'detail': 'Staff with this email already exists!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


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
        message = {'detail': 'Something went wrong'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


def getListById(request, pk):
    user = request.user
    company_obj = CompanyProfile.objects.get(user=user)
    try:
        list = List.objects.get(id=pk)
        serializer = ListSerializer(list, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)