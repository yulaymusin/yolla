from django.urls import path, re_path
from . import views as v

app_name = 'jumbotron'

urlpatterns = [
    path('list', v.List.as_view(), name='list'),  # superuser only
    path('new', v.New.as_view(), name='new'),  # superuser only
    re_path(r'^update/(?P<pk>\d+)$', v.Update.as_view(), name='update'),  # superuser only
    re_path(r'^read/(?P<pk>\d+)$', v.read, name='read'),  # superuser only
]
