from django.contrib import admin


class CommentBoxAdminBase(admin.ModelAdmin):

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.user = request.user

        formset.save()
