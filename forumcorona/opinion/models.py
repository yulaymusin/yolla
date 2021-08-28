from django.db import models
from django.utils.translation import ugettext_lazy as _
from forumcorona.participant.models import Participant
from forumcorona.topic.models import Topic


opinion_statuses = (
    (1, '1. Published'),
    (2, '2. Preparing to publish'),
    (3, '3. Accepted'),
    (4, '4. Posted by publisher'),
    (5, '5. Draft'),
    (6, '6. Rejected'),
    (7, '7. Deleted by publisher'),
)
opinion_statuses_to_display_to_participant = (
    (1, _('Published')),
    (2, _('Preparing to publish')),
    (3, _('Accepted by moderator')),
    (4, _('Sent for publication')),
    (6, _('Rejected by moderator')),
    (7, _('Canceled to publish')),
)


def opinion_verbose_status(status_num, to_display_to_participant=False):
    if to_display_to_participant is False:
        for status in opinion_statuses:
            if status[0] == status_num:
                return status[1]
    for status in opinion_statuses_to_display_to_participant:
        if status[0] == status_num:
            return status[1]


class Opinion(models.Model):
    class Meta:
        db_table = 'opinion'
        ordering = ('pk',)

    recorded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.PositiveSmallIntegerField(db_index=True, default=4, choices=opinion_statuses)
    reason_for_rejection = models.TextField(blank=True)

    publisher = models.ForeignKey(Participant, models.PROTECT)
    topic = models.ForeignKey(Topic, models.PROTECT)

    apex = models.ForeignKey('self', models.PROTECT, null=True)
    apex_language = models.CharField(max_length=20)

    en_text = models.TextField('Text in English', blank=True)
    zh_hans_text = models.TextField('Text in Chinese Simplified', blank=True)
    zh_hant_text = models.TextField('Text in Chinese Traditional', blank=True)
    es_text = models.TextField('Text in Spanish', blank=True)
    ar_text = models.TextField('Text in Arabic', blank=True)
    fr_text = models.TextField('Text in French', blank=True)
    ru_text = models.TextField('Text in Russian', blank=True)


class OpinionAttachment(models.Model):
    class Meta:
        db_table = 'opinion_attachment'

    opinion = models.ForeignKey(Opinion, models.PROTECT)
    document = models.FileField(upload_to='%Y-%m-%d/')
    original_label = models.CharField(max_length=200, default='')
    md5 = models.CharField(db_index=True, max_length=32, default='')
    size = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)
