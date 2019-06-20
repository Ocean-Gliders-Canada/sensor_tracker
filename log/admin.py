from django.contrib.admin.models import LogEntry
from django.contrib import admin


@admin.register(LogEntry)
class PlatformTypeAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_time', 'message', 'target_obj', 'action')

    def get_queryset(self, request):
        user = request.user
        qs = super(PlatformTypeAdmin, self).get_queryset(request).order_by('action_time')
        if not user.is_superuser:
            qs = qs.filter(user=user)
        qs = qs.prefetch_related('content_type')
        return qs

    def message(self, instance):
        return """<a href="{}">{}</a>""".format(instance.get_admin_url(), instance.change_message)

    message.allow_tags = True

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
