from django.urls import path, re_path
from . import views as v, views_media as media

app_name = 'article'

urlpatterns = [
    path('list', v.List.as_view(), name='list'),  # superuser only
    path('new', v.New.as_view(), name='new'),  # superuser only
    re_path(r'^update/(?P<pk>\d+)$', v.Update.as_view(), name='update'),  # superuser only
    re_path(r'^read/(?P<pk>\d+)$', v.read, name='read'),  # superuser only

    re_path(r'^upload_images$', media.upload_images, name='upload_images'),  # superuser only
    re_path(r'^delete_image/(?P<media_pk>\d+)$', media.delete_image, name='delete_image'),  # superuser only
]
