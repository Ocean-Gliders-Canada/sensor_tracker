from general.models import Manufacturer, Institution, Project
from instruments.models import Instrument, InstrumentComment, InstrumentOnPlatform, Sensor
from platforms.models import PlatformType, Platform, PlatformPowerType, PlatformDeployment, PlatformDeploymentComment, \
    PlatformComment
from rest_framework.serializers import ModelSerializer

from collections import OrderedDict




class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentSerializer(ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentCommentSerializer(ModelSerializer):
    class Meta:
        model = InstrumentComment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class InstrumentOnPlatformSerializer(ModelSerializer):
    class Meta:
        model = InstrumentOnPlatform
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformCommentSerializer(ModelSerializer):
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


class PlatformTypeSerializer(ModelSerializer):
    class Meta:
        model = PlatformType
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformPowerTypeSerializer(ModelSerializer):
    class Meta:
        model = PlatformPowerType
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformDeploymentSerializer(ModelSerializer):
    class Meta:
        model = PlatformDeployment
        fields = '__all__'
        read_only = ('created_date', 'modified_date')


class PlatformDeploymentCommentSerializer(ModelSerializer):
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
