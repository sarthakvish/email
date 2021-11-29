from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email_app.models.subscribers_models import Subscribers
from email_app.serializers import SubscribersSerializer


@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getSubscribers(request):
    user = Subscribers.objects.all()
    serializer = SubscribersSerializer(user, many=True)
    return Response(serializer.data)
