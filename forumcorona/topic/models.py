from django.db import models
from forumcorona.common import sql_custom as sql
from forumcorona.common.language import lang
from forumcorona.category.models import Category


class Topic(models.Model):
    class Meta:
        db_table = 'topic'
        ordering = ('-updated', '-pk')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField()
    published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, models.PROTECT)

    en_name = models.CharField('Name in English', max_length=200)
    zh_hans_name = models.CharField('Name in Chinese Simplified', max_length=200, blank=True)
    zh_hant_name = models.CharField('Name in Chinese Traditional', max_length=200, blank=True)
    es_name = models.CharField('Name in Spanish', max_length=200, blank=True)
    ar_name = models.CharField('Name in Arabic', max_length=200, blank=True)
    fr_name = models.CharField('Name in French', max_length=200, blank=True)
    ru_name = models.CharField('Name in Russian', max_length=200, blank=True)

    en_description = models.CharField('Description in English', max_length=500)
    zh_hans_description = models.CharField('Description in Chinese Simplified', max_length=500, blank=True)
    zh_hant_description = models.CharField('Description in Chinese Traditional', max_length=500, blank=True)
    es_description = models.CharField('Description in Spanish', max_length=500, blank=True)
    ar_description = models.CharField('Description in Arabic', max_length=500, blank=True)
    fr_description = models.CharField('Description in French', max_length=500, blank=True)
    ru_description = models.CharField('Description in Russian', max_length=500, blank=True)

    def __str__(self):
        return self.en_name


def get_topics_grouped_by_category_id(categories_of_topics, select_limit=3):
    topics = {}
    query = []
    for topic_category_id in categories_of_topics:
        topics[topic_category_id] = []
        q = '(SELECT "topic"."id", "topic"."slug", "topic"."category_id", "topic"."{lang_name}" FROM "topic" WHERE' \
            ' ("topic"."category_id" = {category_id} AND "topic"."published") ORDER BY "topic"."updated" DESC,' \
            ' "topic"."id" DESC LIMIT {limit_int})' \
            .format(lang_name=lang('_name'), category_id=topic_category_id, limit_int=select_limit)
        query.append(q)
    query = ' UNION ALL '.join(query)
    if query == '':
        return {}
    topics_values = sql.sql(query=query)
    for topic in topics_values:
        # topics[topic['category_id']].append(topic)
        topics[topic['category_id']].append({
            'id': topic['id'],
            'slug': topic['slug'],
            # 'category_id': topic['category_id'],
            'name': topic[lang('_name')],
        })
    return topics
