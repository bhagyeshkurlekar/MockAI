""" Serializers for Models in Core App """
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import CanvasUser, Conversation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import authenticate
# from django.utils.translation import ugettext_lazy as _

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def uppercase_validate(password):
    if not re.findall('[A-Z]', password):
        raise ValidationError(
            _("The password must contain at least 1 uppercase letter, A-Z."),
            code='password_no_upper',
        )


def lowercase_validate(password):
    if not re.findall('[a-z]', password):
        raise ValidationError(
            _("The password must contain at least 1 lowercase letter, a-z."),
            code='password_no_lower',
        )


class RegisterSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=320, min_length=3)
    password = serializers.CharField(max_length=100, min_length=8,
                                     label=_("Password"),
                                     style={'input_type': 'password'},
                                     trim_whitespace=False,
                                     validators=[uppercase_validate, lowercase_validate])

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    pincode = serializers.IntegerField(validators=[MaxValueValidator(999999)])

    def create(self, validated_data):
        user = CanvasUser.objects.create_user(username=validated_data['email'], email=validated_data['email'], password=validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'], phone_number=validated_data['phone_number'], pincode=validated_data['pincode'])
        return user

    class Meta:
        model = CanvasUser
        fields = ('id', 'create_date', 'update_date', 'email', 'first_name', 'last_name', 'address', 'city', 'state', 'country', 'phone_number', 'pincode', 'password')


class LoginSerializer(ModelSerializer):

    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:

            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    class Meta:
        model = CanvasUser
        fields = ('email', 'password')


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
