from django.contrib import admin


class CommentBoxAdminBase(admin.ModelAdmin):

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.user = request.user

        formset.save()


class BaseCommentBoxInline(admin.TabularInline):
    extra = 0
    readonly_fields = ('user', 'created_date', 'modified_date')

    fields = ('user', 'created_date', 'modified_date', 'event_time', 'comment')
