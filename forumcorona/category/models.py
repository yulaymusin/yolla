from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'category'
        ordering = ('order_by_this', 'pk')

    order_by_this = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = models.SlugField()
    apex = models.ForeignKey('self', models.PROTECT, null=True, blank=True)
    show_in_top_nav = models.BooleanField(default=False)

    en_name = models.CharField('Name in English', max_length=200)
    zh_hans_name = models.CharField('Name in Chinese Simplified', max_length=200, blank=True)
    zh_hant_name = models.CharField('Name in Chinese Traditional', max_length=200, blank=True)
    es_name = models.CharField('Name in Spanish', max_length=200, blank=True)
    ar_name = models.CharField('Name in Arabic', max_length=200, blank=True)
    fr_name = models.CharField('Name in French', max_length=200, blank=True)
    ru_name = models.CharField('Name in Russian', max_length=200, blank=True)

    def __str__(self):
        return self.en_name
