from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializerMeta:
    model = User
    fields = ('id', 'username', 'email', 'password', 'password2')
    extra_kwargs = {
        'password': {'write_only': True},
    }


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta(UserSerializerMeta):
        ...

    def validate_password2(self, password2):
        if self.initial_data['password'] != password2:
            raise ValidationError(_('Passwords do not match.'))
        return password2

    def validate(self, attrs):
        if not self.instance and not attrs.get('password2'):
            try:
                self.fields['password2'].fail('required')
            except ValidationError as exc:
                raise ValidationError({'password2': exc.detail})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return self._create_user(validated_data)

    def _create_user(self, data):
        return User.objects.create_user(**data)


class StaffSerializer(UserSerializer):
    class Meta(UserSerializerMeta):
        ...

    def _create_user(self, data):
        return User.objects.create_staff(**data)


class ChangePasswordSerializer(UserSerializer):
    old_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, old_password):
        errors = []
        if not self.instance.check_password(old_password):
            errors.append(_('Old password do not match.'))
        if old_password == self.initial_data['password']:
            errors.append(_('Your new password must be different from your previous password.'))
        if errors:
            raise ValidationError(errors)
        return old_password

    class Meta:
        model = User
        fields = ('password', 'password2', 'old_password')
        extra_kwargs = {'password': {'write_only': True}}
