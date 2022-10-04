from django.urls import path, re_path
from . import views as v, views_reply as reply, views_attachment as attachment, views_read as read

app_name = 'opinion'

urlpatterns = [
    path('list', v.List.as_view(), name='list'),  # staff
    re_path(r'^new/(?P<topic_slug>[\w-]+)$', v.New.as_view(), name='new'),  # superuser only
    re_path(r'^update/(?P<pk>\d+)$', v.Update.as_view(), name='update'),  # staff
    re_path(r'^read/(?P<pk>\d+)$', v.read, name='read'),  # staff

    re_path(r'^reply_to_(?P<reply_to_opinion_pk>\d+)$', reply.Reply.as_view(), name='reply'),  # participant
    re_path(r'^edit_(?P<pk>\d+)$', reply.Edit.as_view(), name='edit'),  # participant
    re_path(r'^cancel_(?P<pk>\d+)$', reply.cancel, name='cancel'),  # participant

    re_path(r'^attach_documents_(?P<opinion_pk>\d+)$', attachment.attach_documents, name='attach_documents'),  # participant
    re_path(r'^delete_document_(?P<attachment_pk>\d+)$', attachment.delete_document, name='delete_document'),  # participant
    re_path(r'^documents_(?P<opinion_pk>\d+)$', attachment.zip_documents, name='zip_documents'),  # public

    path('replies', read.Replies.as_view(), name='replies'),  # participant
    re_path(r'^your_reply_(?P<pk>\d+)$', read.your_reply, name='your_reply'),  # participant
    re_path(r'^(?P<topic_slug>[\w-]+)$', read.Topic.as_view(), name='topic'),  # public
]
