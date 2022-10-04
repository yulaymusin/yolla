from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from yolla.common import mixins as mix
from yolla.common.utils import lang
from . import forms as f
from . import models as m


class Reply(LoginRequiredMixin, mix.MsgInFormValid, FormView):
    form_class = f.ReplyEditForm
    template_name = 'opinion/reply.html'
    success_message = _('Sent for publication')
    reply_to_opinion_values = None
    previous_reply_values = None
    reply_object = None

    def get_initial(self):
        self.reply_to_opinion_values = get_object_or_404(
            m.Opinion.objects.values(
                'recorded',  # blockquote
                'topic_id',  # def form_valid
                publisher_name=F('publisher_id__name'),  # blockquote
                topic_slug=F('topic_id__slug'),  # breadcrumbs
                topic_category_apex_slug=F('topic_id__category_id__apex_id__slug'),  # breadcrumbs
                topic_category_apex_name=F('topic_id__category_id__apex_id__'+lang('_name')),  # breadcrumbs
                topic_category_slug=F('topic_id__category_id__slug'),  # breadcrumbs
                topic_category_name=F('topic_id__category_id__'+lang('_name')),  # breadcrumbs
                topic_name=F('topic_id__'+lang('_name')),  # breadcrumbs
                text=F(lang('_text')),  # blockquote
            ),
            pk=self.kwargs.get('reply_to_opinion_pk')
        )
        self.previous_reply_values = m.Opinion.objects.values(
            'recorded',  # panel
            'status',  # previous_reply_verbose_status
            publisher_name=F('publisher_id__name'),  # panel
            text=F(lang('_text')),  # panel
        ).filter(status__in=(1, 2, 3, 4), publisher=self.request.user, apex_id=self.kwargs.get('reply_to_opinion_pk'),)[:1]
        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': _('Reply'),
            'submit_btn': _('Reply'),
            'opinion': self.reply_to_opinion_values,
            'l1': self.request.user.l1,
            'l2': self.request.user.l2,
            'previous_reply': self.previous_reply_values,
            'previous_reply_verbose_status': m.opinion_verbose_status(
                self.previous_reply_values[0]['status'], to_display_to_participant=True) if self.previous_reply_values else '',
        })
        return context

    def form_valid(self, form):
        if self.previous_reply_values:
            return self.form_invalid(form)

        cd = form.cleaned_data
        self.reply_object = m.Opinion.objects.create(
            publisher=self.request.user,
            topic_id=self.reply_to_opinion_values['topic_id'],

            apex_id=self.kwargs.get('reply_to_opinion_pk'),
            apex_language=self.request.user.l1,

            en_text=cd.get('en_text'),
            zh_hans_text=cd.get('zh_hans_text'),
            es_text=cd.get('es_text'),
            ar_text=cd.get('ar_text'),
            fr_text=cd.get('fr_text'),
            ru_text=cd.get('ru_text'),
        )
        messages.info(self.request, _('Before your reply is accepted by moderator, you can edit, unpublish and manage documents.'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('opinion:your_reply', kwargs={'pk': self.reply_object.id})


class Edit(LoginRequiredMixin, mix.MsgInFormValid, FormView):
    form_class = f.ReplyEditForm
    template_name = 'opinion/edit.html'
    success_message = _('Edits saved.')
    opinion_values = None

    def get_initial(self):
        self.opinion_values = get_object_or_404(
            m.Opinion.objects.values(
                'recorded',  # panel
                'status',  # def form_valid
                'en_text', 'zh_hans_text', 'es_text', 'ar_text', 'fr_text', 'ru_text',  # form
                publisher_name=F('publisher_id__name'),  # panel
                topic_category_apex_name=F('topic_id__category_id__apex_id__'+lang('_name')),  # breadcrumbs
                topic_category_name=F('topic_id__category_id__'+lang('_name')),  # breadcrumbs
                topic_name=F('topic_id__'+lang('_name')),  # breadcrumbs
                apex_recorded=F('apex_id__recorded'),  # blockquote
                apex_publisher_name=F('apex_id__publisher_id__name'),  # blockquote
                apex_text=F('apex_id__'+lang('_text')),  # blockquote
                text=F(lang('_text')),  # panel
            ),
            pk=self.kwargs.get('pk'), publisher=self.request.user
        )
        initial = super().get_initial()
        initial.update({
            'en_text': self.opinion_values['en_text'],
            'zh_hans_text': self.opinion_values['zh_hans_text'],
            'es_text': self.opinion_values['es_text'],
            'ar_text': self.opinion_values['ar_text'],
            'fr_text': self.opinion_values['fr_text'],
            'ru_text': self.opinion_values['ru_text'],
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': _('Editing your reply'),
            'submit_btn': _('Save'),
            'opinion': self.opinion_values,
            'opinion_verbose_status': m.opinion_verbose_status(self.opinion_values['status'], to_display_to_participant=True),
            'l1': self.request.user.l1,
            'l2': self.request.user.l2,
        })
        return context

    def form_valid(self, form):
        if self.opinion_values['status'] != 4:
            return self.form_invalid(form)

        cd = form.cleaned_data
        m.Opinion.objects.filter(pk=self.kwargs.get('pk')).update(
            en_text=cd.get('en_text'),
            zh_hans_text=cd.get('zh_hans_text'),
            es_text=cd.get('es_text'),
            ar_text=cd.get('ar_text'),
            fr_text=cd.get('fr_text'),
            ru_text=cd.get('ru_text'),
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('opinion:your_reply', kwargs={'pk': self.kwargs.get('pk')})


@login_required
def cancel(request, pk):
    if request.method == 'POST':
        m.Opinion.objects.filter(pk=pk, status=4, publisher=request.user).update(status=7)
        messages.info(request, _('Publication of your reply has been canceled.'))
        return redirect(reverse_lazy('opinion:replies'))

    opinion_values = get_object_or_404(
        m.Opinion.objects.values(
            'recorded',  # panel
            publisher_name=F('publisher_id__name'),  # panel
            topic_category_apex_name=F('topic_id__category_id__apex_id__' + lang('_name')),  # breadcrumbs
            topic_category_name=F('topic_id__category_id__' + lang('_name')),  # breadcrumbs
            topic_name=F('topic_id__' + lang('_name')),  # breadcrumbs
            apex_recorded=F('apex_id__recorded'),  # blockquote
            apex_publisher_name=F('apex_id__publisher_id__name'),  # blockquote
            apex_text=F('apex_id__' + lang('_text')),  # blockquote
            text=F(lang('_text')),  # panel
        ),
        pk=pk, status=4, publisher=request.user
    )
    return render(request, 'opinion/cancel.html', {
        'label': _('Canceling the publication of your reply'),
        'opinion': opinion_values,
    })
