from rest_framework import serializers

from template import models


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseMixin
        fields = '__all__'
