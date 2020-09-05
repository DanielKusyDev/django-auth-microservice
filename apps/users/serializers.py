from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password2(self, password2):
        if self.initial_data['password'] != password2:
            raise ValidationError(_('Passwords do not match.'))
        return password2

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)
