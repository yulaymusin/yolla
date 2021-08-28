from django.conf import settings
from django.db import models
from django.db.models import F
from forumcorona.common.utils import lang
from forumcorona.category.models import Category
from forumcorona.topic.models import Topic


class Jumbotron(models.Model):
    class Meta:
        db_table = 'jumbotron'
        ordering = ('-pk',)

    page_home = models.BooleanField(default=False)
    category = models.ForeignKey(Category, models.PROTECT, null=True, blank=True)
    topic = models.ForeignKey(Topic, models.PROTECT, null=True, blank=True)

    en_content = models.CharField('Content in English', max_length=200)
    zh_hans_content = models.CharField('Content in Chinese Simplified', max_length=200)
    zh_hant_content = models.CharField('Content in Chinese Traditional', max_length=200)
    es_content = models.CharField('Content in Spanish', max_length=200)
    ar_content = models.CharField('Content in Arabic', max_length=200)
    fr_content = models.CharField('Content in French', max_length=200)
    ru_content = models.CharField('Content in Russian', max_length=200)


def get_jumbotron_for_context(user, category_id_only=None, topic_id_only=None):
    if user.is_authenticated and user.l2:
        j = Jumbotron.objects.values(l1=F(lang('_content')), l2=F(user.l2.replace('-', '_') + '_content'),)
    else:
        j = Jumbotron.objects.values_list(lang('_content'), flat=True)

    if not category_id_only and not topic_id_only:
        j = j.filter(page_home=True)[:1]
    elif category_id_only and not topic_id_only:
        j = j.filter(category_id=category_id_only)[:1]
    elif not category_id_only and topic_id_only:
        j = j.filter(topic_id=topic_id_only)[:1]
    else:
        j = None

    if j and user.is_authenticated and user.l2:
        jumbotron = {'l1_content': j[0]['l1'], 'l2_content': j[0]['l2'], }
        for language in settings.LANGUAGES:
            if language[0] == user.l1:
                jumbotron.update({'l1_code': language[0], 'l1_dir': 'rtl' if language[0] in settings.RTL_LANGUAGES_CODES else 'ltr'})
            if language[0] == user.l2:
                jumbotron.update({'l2_code': language[0], 'l2_dir': 'rtl' if language[0] in settings.RTL_LANGUAGES_CODES else 'ltr'})
        return jumbotron
    elif j:
        return {'l1_content': j[0]}

    return None
