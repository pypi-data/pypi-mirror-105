from django.urls import path

from template import views


urlpatterns = [
    path('template', views.TemplateListCreateView.as_view(), name='template-lc'),
    path('template/<uuid:id>', views.TemplateRetrieveUpdateDestroyView.as_view(), name='template-rud'),
]
