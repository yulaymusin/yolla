from django.urls import path, re_path
from . import views as v

app_name = 'topic'

urlpatterns = [
    path('list', v.List.as_view(), name='list'),  # superuser only
    path('new', v.New.as_view(), name='new'),  # superuser only
    re_path(r'^edit/(?P<pk>\d+)$', v.Edit.as_view(), name='edit'),  # superuser only

    re_path(r'^(?P<category_slug>[\w-]+)$', v.Category.as_view(), name='category'),  # public
]
