from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import list_route
from rest_framework.renderers import TemplateHTMLRenderer

from django.http import HttpResponseRedirect


class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class AddFormMixin(object):
    """
    以表单的方式创建一个model实例。
    """
    add_serializer_class = None
    add_success_url = None

    def add(self, request):
        if request.method == 'GET':
            serializer = self.get_add_serializer();
            return Response({'serializer': serializer})
        elif request.method == 'POST':
            serializer = self.get_add_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({'serializer': serializer})
            self.perform_add(serializer)
            return HttpResponseRedirect(self.get_add_success_url() + '?id=%s' % serializer.data['id'])

    def get_add_serializer(self, *args, **kwargs):
        return self.add_serializer_class(*args, **kwargs)

    def get_add_success_url(self, *args, **kwargs):
        return self.add_success_url

    def perform_add(self, serializer):
        serializer.save()