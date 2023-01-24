from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework import serializers
from user.models import User
from allauth.socialaccount.models import SocialAccount


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        print('serialized data')

        return data

class MyTokenObtainSerializer(TokenObtainSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    social_account = serializers.PrimaryKeyRelatedField(queryset=SocialAccount.objects.all())

    class Meta:
        fields = ('user', 'social_account')

    def validate(self, attrs):
        print('validate')
        user = attrs['user']
        social_account = attrs['social_account']
        if user and social_account:
            if not user.is_active:
                msg = ('User account is disabled.')
                raise serializers.ValidationError(msg, code='authorization')
            if not social_account.is_active:
                msg = ('Social account is disabled.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        # return super().validate(attrs)