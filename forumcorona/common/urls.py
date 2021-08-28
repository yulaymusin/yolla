from django.urls import path
from . import views as v

app_name = 'common'

urlpatterns = [
    path('', v.categories_with_topics, name='page_home'),
]
