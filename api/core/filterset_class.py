"""
All filterset class are built by factory now
"""

# from general import models as general
# from instruments import models as instruments
# from platforms import models as platforms
#
# from django_filters import rest_framework as filters
#
#
# class InstrumentFilter(filters.FilterSet):
#     identifier = filters.CharFilter(field_name="identifier",
#                                     help_text="The name used to identify this instrument in the raw data. IE: SATCTD7229, sci_water")
#     short_name = filters.CharFilter(field_name="short_name",
#                                     help_text="The short, general name for the instrument. IE: ctd, fluorometer")
#     long_name = filters.CharFilter(field_name="long_name", help_text="The full name for the instrument")
#     serial = filters.CharFilter(field_name="serial", help_text="The serial number of the instrument")
#     manufacturer = filters.CharFilter(field_name="manufacturer", help_text="manufacturer name")
#
#     class Meta:
#         model = instruments.Instrument
#         fields = ["identifier", "short_name", "long_name", "serial", "manufacturer"]
