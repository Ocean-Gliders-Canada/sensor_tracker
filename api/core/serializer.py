from collections import OrderedDict

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from general import models as general
from instruments import models as instruments
from platforms import models as platforms


class ManufacturerSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = general.Manufacturer
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstitutionSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = general.Institution
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = instruments.Instrument
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class ProjectSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = general.Project
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentCommentSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = instruments.InstrumentComment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentOnPlatformSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = instruments.InstrumentOnPlatform
        fields = '__all__'
        read_only = ('created_date', 'modified_date')

class SensorSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = instruments.Sensor
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformCommentSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = platforms.PlatformComment
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


class SensorOnInstrumentSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = instruments.SensorOnInstrument
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformTypeSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = platforms.PlatformType
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = platforms.Platform
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformPowerTypeSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = platforms.PlatformPowerType
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformDeploymentSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = platforms.PlatformDeployment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformDeploymentCommentSerializer(serializers.ModelSerializer):
    modified_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    # Todo: overwrite the deserilizer
    class Meta:
        model = platforms.PlatformDeploymentComment
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
