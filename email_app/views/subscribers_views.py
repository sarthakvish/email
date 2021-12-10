from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Subscribers
from email_app.models.user_models import CompanyProfile
from email_app.serializers import SubscribersSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSubscriber(request):
    user = request.user
    print('sarthak', user)
    company_obj = CompanyProfile.objects.get(user=user)
    data = request.data

    subscriber = Subscribers.objects.create(
        company=company_obj,
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    # current_site = get_current_site(request)
    # email_body = {
    #     'user': user,
    #     'domain': current_site.domain,
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token': account_activation_token.make_token(user),
    # }
    #
    # link = reverse('activate', kwargs={
    #     'uidb64': email_body['uid'], 'token': email_body['token']})
    #
    # email_subject = 'Activate your account'
    #
    # activate_url = 'http://' + current_site.domain + link
    #
    # email_message = EmailMessage(
    #     email_subject,
    #     'Hi ' + user.first_name + ', Please the link below to activate your account \n' + activate_url,
    #     settings.EMAIL_HOST_USER,
    #     ['sarthakvishwakarma6@gmail.com'],
    # )
    # EmailThread(email_message).start()

    serializer = SubscribersSerializer(subscriber, many=False)
    return Response(serializer.data)

    # try:
    #     subscriber = Subscribers.objects.create(
    #         company=company_obj.pk,
    #         name=data['name'],
    #         email=data['email'],
    #         phone=data['phone']
    #     )
    #     # current_site = get_current_site(request)
    #     # email_body = {
    #     #     'user': user,
    #     #     'domain': current_site.domain,
    #     #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     #     'token': account_activation_token.make_token(user),
    #     # }
    #     #
    #     # link = reverse('activate', kwargs={
    #     #     'uidb64': email_body['uid'], 'token': email_body['token']})
    #     #
    #     # email_subject = 'Activate your account'
    #     #
    #     # activate_url = 'http://' + current_site.domain + link
    #     #
    #     # email_message = EmailMessage(
    #     #     email_subject,
    #     #     'Hi ' + user.first_name + ', Please the link below to activate your account \n' + activate_url,
    #     #     settings.EMAIL_HOST_USER,
    #     #     ['sarthakvishwakarma6@gmail.com'],
    #     # )
    #     # EmailThread(email_message).start()
    #
    #     serializer = SubscribersSerializer(subscriber, many=False)
    #     return Response(serializer.data)
    #
    # except:
    #     message = {'detail': 'Staff with this email already exists!'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)


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
