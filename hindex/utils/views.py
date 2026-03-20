import humps
from collections import defaultdict

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# Create your views here.
from .enums import get_enum_classes


class EnumViewset(GenericAPIView):
    """ Return enums for all choice fields
    """

    def get(self, request, *args, **kwargs):
        class_list = get_enum_classes()
        response = defaultdict(list)
        for cls in class_list:
            class_name = humps.camelize(cls.__name__)
            for value, label in cls.choices:
                response[class_name].append(
                    {'value': value, 'label': label}
                )
        return Response(response)
