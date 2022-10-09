from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, re_path
from yolla.common import error_handlers


urlpatterns = [
    re_path(r'^', include('yolla.common.urls')),
    re_path(r'^participants/', include('yolla.participant.urls')),
    re_path(r'^categories/', include('yolla.category.urls', namespace='category')),
    re_path(r'^topics/', include('yolla.topic.urls', namespace='topic')),
    re_path(r'^opinions/', include('yolla.opinion.urls', namespace='opinion')),
    re_path(r'^articles/', include('yolla.article.urls', namespace='article')),
    re_path(r'^jumbotrons/', include('yolla.jumbotron.urls', namespace='jumbotron')),
]

handler403 = error_handlers.status_code_403
handler404 = error_handlers.status_code_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
