from django.conf import settings
from django.db import models
from django.db.models import F
from forumcorona.common.utils import lang
from forumcorona.category.models import Category
from forumcorona.topic.models import Topic

article_statuses = (
    (1, '1. Published'),
    (2, '2. Preparing to publish'),
    (3, '3. Draft'),
)


def article_verbose_status(status_num):
    for status in article_statuses:
        if status[0] == status_num:
            return status[1]


class Article(models.Model):
    class Meta:
        db_table = 'article'
        ordering = ('mobile', 'status', '-page_home', 'category', 'topic', 'pk',)

    mobile = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=3, choices=article_statuses)

    page_home = models.BooleanField(default=False)
    category = models.ForeignKey(Category, models.PROTECT, null=True, blank=True)
    topic = models.ForeignKey(Topic, models.PROTECT, null=True, blank=True)

    en_content = models.TextField('Content in English', blank=True)
    zh_hans_content = models.TextField('Content in Chinese Simplified', blank=True)
    zh_hant_content = models.TextField('Content in Chinese Traditional', blank=True)
    es_content = models.TextField('Content in Spanish', blank=True)
    ar_content = models.TextField('Content in Arabic', blank=True)
    fr_content = models.TextField('Content in French', blank=True)
    ru_content = models.TextField('Content in Russian', blank=True)


class ArticleMedia(models.Model):
    class Meta:
        db_table = 'article_media'
        ordering = ('image',)

    image = models.FileField(upload_to='')
    md5 = models.CharField(max_length=32, default='')
    size = models.PositiveIntegerField(default=0)


def media_url_in_str(article_content):
    return article_content.replace('[MEDIA_URL]', settings.MEDIA_URL)


def get_article_for_context(user, http_user_agent, category_id_only=None, topic_id_only=None):
    if user.is_authenticated and user.l2:
        a = Article.objects.values(l1=F(lang('_content')), l2=F(user.l2 + '_content'),)
    else:
        a = Article.objects.values_list(lang('_content'), flat=True)

    if 'mobile' in http_user_agent.lower():
        a = a.filter(mobile=True)

    if not category_id_only and not topic_id_only:
        a = a.filter(status=1, page_home=True)[:1]
    elif category_id_only and not topic_id_only:
        a = a.filter(status=1, category_id=category_id_only)[:1]
    elif not category_id_only and topic_id_only:
        a = a.filter(status=1, topic_id=topic_id_only)[:1]
    else:
        a = None

    if a and user.is_authenticated and user.l2:
        article = {
            'l1_content': media_url_in_str(a[0]['l1']),
            'l2_content': media_url_in_str(a[0]['l2']),
        }
        for language in settings.LANGUAGES:
            if language[0] == user.l1:
                article.update({'l1_name': language[1]})
            if language[0] == user.l2:
                article.update({'l2_name': language[1]})
        return article
    elif a:
        return {'l1_content': media_url_in_str(a[0])}

    return None
