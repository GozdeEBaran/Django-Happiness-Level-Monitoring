from django.urls import path
from hindex.utils.views import EnumViewset


urlpatterns = [
    path('utils/enums/', EnumViewset.as_view(), name='enums'),
]
