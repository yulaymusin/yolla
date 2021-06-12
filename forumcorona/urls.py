from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from forumcorona.common import error_handlers
from forumcorona.common.views import sitemap_xml


urlpatterns = i18n_patterns(
    url(r'^', include('forumcorona.common.urls')),
    url(r'^participants/', include('forumcorona.participant.urls')),
    url(r'^categories/', include('forumcorona.category.urls', namespace='category')),
    url(r'^topics/', include('forumcorona.topic.urls', namespace='topic')),
    url(r'^opinions/', include('forumcorona.opinion.urls', namespace='opinion')),
    url(r'^searches/', include('forumcorona.search.urls', namespace='search')),
    url(r'^articles/', include('forumcorona.article.urls', namespace='article')),
    url(r'^jumbotron/', include('forumcorona.jumbotron.urls', namespace='jumbotron')),
)
urlpatterns += [
    url(r'^sitemap.xml$', sitemap_xml, name='sitemap_xml'),
]

handler403 = error_handlers.eh403
handler404 = error_handlers.eh404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
