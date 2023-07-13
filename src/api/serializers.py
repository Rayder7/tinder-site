import djoser.serializers
from django.contrib.auth import get_user_model

from api.utils import add_watermark_image

User = get_user_model()


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'sex',
                  'longitude', 'latitude', 'password', 'email')

    def create(self, validated_data):
        avatar = validated_data.pop('avatar')
        avatar = add_watermark_image(avatar)
        validated_data['avatar'] = avatar
        return super().create(validated_data)


class UserSerializer(djoser.serializers.UserSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'sex',
                  'longitude', 'latitude')
