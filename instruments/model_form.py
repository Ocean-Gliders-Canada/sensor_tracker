from django.forms import ModelForm
from django import forms
from django.db.models import Q

from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    Instrument,
    InstrumentOnPlatform,
    Sensor,
    SensorOnInstrument,
    InstrumentCommentBox
)
from common.utilities import make_edit_link
from django.utils.safestring import mark_safe
from common.utilities import qs_time_overlap


class InstrumentOnPlatformForm(ModelForm):
    class Meta:
        model = InstrumentOnPlatform
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        include_in_output = cleaned_data.get("include_in_output")
        long_name = cleaned_data.get("long_name")

        if include_in_output and not long_name:
            # Only do something if both fields are valid so far.

            raise forms.ValidationError(
                "Long name must be given when included in output checked"
            )
        return self.cleaned_data


class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'


class SensorOnInstrumentForm(ModelForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if self.initial:
            self.fields['sensor'].disabled = True
            self.fields['instrument'].disabled = True

    class Meta:
        model = SensorOnInstrument
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        instrument = cleaned_data.get("instrument")
        sensor = cleaned_data.get("sensor")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        base_soi_qs = SensorOnInstrument.objects.filter(instrument=instrument, sensor=sensor)
        self_instance = self.instance
        soi_qs_overlap = qs_time_overlap(base_soi_qs, start_time, end_time)
        the_id = self_instance.id
        if the_id:
            soi_qs_overlap = soi_qs_overlap.filter(~Q(pk=the_id))

        soi_qs_overlap_count = soi_qs_overlap.count()

        if soi_qs_overlap_count != 0:
            msg = "You can't save this table since it overlap with \n"
            for soi in soi_qs_overlap:
                msg = msg + "{} {} {}\n".format(soi.instrument.identifier, soi.sensor.identifier,
                                                "<a href=\"{}\">sensor_on_instrument</a>".format(make_edit_link(soi)))

            raise forms.ValidationError(
                mark_safe(msg)
            )
        return self.cleaned_data


class InstrumentCommentBoxForm(ModelForm):
    class Meta:
        model = InstrumentCommentBox
        fields = ('instrument',)
