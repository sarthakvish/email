from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from email_app.models.user_models import CompanyProfile, StaffUsers
from email_app.models.subscribers_models import Subscribers, Template, List, Campaigns, GetList
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', ]

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


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ['id', 'company_id', 'company_name', 'address', 'user']

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializerWithToken(user, many=False)
        return serializer.data


class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers
        fields = '__all__'


class StaffProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    company_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data

    def get_company_id(self, obj):
        company_id = obj.company_id
        serializer = CompanyProfileSerializer(company_id, many=False)
        return serializer.data


class StaffSerializerWithUser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StaffUsers
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class ListSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    subscriber = SubscribersSerializer(many=True)

    class Meta:
        model = List
        fields = '__all__'


class CampaignSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    list = ListSerializer(many=True)

    class Meta:
        model = Campaigns
        fields = '__all__'


class CampaignSerializerWithoutList(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Campaigns
        fields = '__all__'


class GetListSerializers(serializers.ModelSerializer):
    class Meta:
        model = GetList
        fields = ('title', 'body')
