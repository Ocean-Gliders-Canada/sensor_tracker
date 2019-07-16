from general.models import Manufacturer, Institution, Project
from instruments.models import Instrument, InstrumentComment, InstrumentOnPlatform, Sensor
from platforms.models import PlatformType, Platform, PlatformPowerType, PlatformDeployment, PlatformDeploymentComment, \
    PlatformComment
from rest_framework import serializers

from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentComment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentOnPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentOnPlatform
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformComment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'user' in ret:
            if type(ret['user']) is not int:
                new_user_dict = OrderedDict()
                new_user_dict["id"] = ret['user']["id"]
                new_user_dict["username"] = ret['user']["username"]
                ret['user'] = new_user_dict
        return ret


class PlatformTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformType
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformPowerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformPowerType
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformDeployment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformDeploymentCommentSerializer(serializers.ModelSerializer):
    # Todo: overwrite the deserilizer
    class Meta:
        model = PlatformDeploymentComment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'user' in ret:
            if type(ret['user']) is not int:
                new_user_dict = OrderedDict()
                new_user_dict["id"] = ret['user']["id"]
                new_user_dict["username"] = ret['user']["username"]
                ret['user'] = new_user_dict
        return ret


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), required=False)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=False
    )
    token = serializers.CharField(
        label=_("token"),
        allow_null=True,
        required=False
    )

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        token = attrs.get('token', None)
        user = None
        token_str = None
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        elif token:
            try:
                token = Token.objects.get(key=token)
            except ObjectDoesNotExist:
                msg = _('Failed to validated with provided token.')
                raise serializers.ValidationError(msg, code='authorization')
            else:
                token_str = token.key
        else:
            msg = _('Must include ("username" and "password") or "token".')
            raise serializers.ValidationError(msg, code='authorization')

        if user:
            attrs['user'] = user
        else:
            attrs['token'] = token_str
        return attrs
