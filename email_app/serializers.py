from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from email_app.models.user_models import CompanyProfile


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


#
# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#
#         fields = '__all__'
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     reviews = serializers.SerializerMethodField(read_only=True) # adding extrafield, product k sath sath
#
#     class Meta:
#
#         fields = '__all__'
#
#     def get_reviews(self, obj):
#         reviews = obj.review_set.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return serializer.data
#
#
# class ShippingAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#
#         fields = '__all__'
#
#
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = '__all__'
#
#
class CompanyProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
