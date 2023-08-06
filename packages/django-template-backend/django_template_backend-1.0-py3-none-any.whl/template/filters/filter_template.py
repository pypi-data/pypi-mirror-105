from django_filters import rest_framework as django_filters

from template import models


class TemplateFilter(django_filters.FilterSet):
    class Meta:
        model = models.Template
        fields = {}
