from template import models
from template.serializers import BaseSerializer


class TemplateSerializer(BaseSerializer):
    class Meta:
        model = models.Template
        fields = '__all__'
