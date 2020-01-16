from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.utils.html import format_html
from custom_admin import admin as custom_admin_site


@admin.register(LogEntry)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_time', 'message', 'target_obj', 'action',)

    list_display_links = None

    def get_queryset(self, request):
        user = request.user
        qs = super(LogAdmin, self).get_queryset(request).order_by('action_time')
        if not user.is_superuser:
            qs = qs.filter(user=user)
        qs = qs.prefetch_related('content_type')
        return qs

    def message(self, instance):

        the_str = '<a href=\"{}\">{}</a>'.format(instance.get_admin_url(), instance)
        return format_html(the_str)

    def action(self, instance):
        """
        ADDITION = 1
        CHANGE = 2
        DELETION = 3
        """
        action_flag = instance.action_flag
        if action_flag == 1:
            return "ADDITION"
        elif action_flag == 2:
            return "CHANGE"
        elif action_flag == 3:
            return "DELETION"
        else:
            return "UNKNOWN ACTION {}".format(action_flag)

    def target_obj(self, instance):
        return instance.content_type

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


custom_admin_site.site.register(LogEntry, LogAdmin)
