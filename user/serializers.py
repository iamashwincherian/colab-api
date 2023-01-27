from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'name', 'is_staff', 'is_active', 'date_joined', 'last_login')
