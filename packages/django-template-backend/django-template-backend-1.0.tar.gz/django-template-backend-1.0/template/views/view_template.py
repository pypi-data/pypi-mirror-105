from rest_framework import generics

from template import serializers, models, filters


class TemplateListCreateView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.TemplateSerializer
    queryset = models.Template.objects.all()
    filterset_class = filters.TemplateFilter


class TemplateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.TemplateSerializer
    queryset = models.Template.objects.all()
