from django.urls import path, re_path
from . import views as v

app_name = 'category'

urlpatterns = [
    path('list', v.List.as_view(), name='list'),  # superuser only
    path('new', v.New.as_view(), name='new'),  # superuser only
    re_path(r'^edit/(?P<pk>\d+)$', v.Edit.as_view(), name='edit'),  # superuser only

    re_path(r'^(?P<slug>[\w-]+)$', v.container, name='container'),  # public
]
