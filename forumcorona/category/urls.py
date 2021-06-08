from django.conf.urls import url
from . import views as v

app_name = 'category'

urlpatterns = [
    url(r'^list$', v.List.as_view(), name='list'),  # superuser only
    url(r'^new$', v.New.as_view(), name='new'),  # superuser only
    url(r'^edit/(?P<pk>\d+)$', v.Edit.as_view(), name='edit'),  # superuser only

    url(r'^(?P<slug>[\w-]+)$', v.container, name='container'),  # public
]
