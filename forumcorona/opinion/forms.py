from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models as m


class ReplyEditForm(forms.ModelForm):
    class Meta:
        model = m.Opinion
        fields = ('en_text', 'zh_hans_text', 'zh_hant_text', 'es_text', 'ar_text', 'fr_text', 'ru_text')
        labels = {
            'en_text': _('Reply in English'),
            'zh_hans_text': _('Reply in Chinese Simplified'),
            'zh_hant_text': _('Reply in Chinese Traditional'),
            'es_text': _('Reply in Spanish'),
            'ar_text': _('Reply in Arabic'),
            'fr_text': _('Reply in French'),
            'ru_text': _('Reply in Russian'),
        }
