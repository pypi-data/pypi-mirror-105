from django.contrib import admin

from template.models import Template


class TemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Template, TemplateAdmin)
