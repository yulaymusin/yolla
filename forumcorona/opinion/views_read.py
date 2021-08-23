from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from forumcorona.common import mixins as mix
from forumcorona.common.utils import lang
from forumcorona.article.models import get_article_for_context
from forumcorona.jumbotron.models import get_jumbotron_for_context
from .views import FilterByTopicAndStatusMixin
from . import models as m


class Replies(LoginRequiredMixin, mix.ListViewContextPaginated, FilterByTopicAndStatusMixin, ListView):
    model = m.Opinion
    template_name = 'opinion/replies.html'
    # topics_categories = {
    #     'Subcategory 1 of first category': {
    #         1: '1-1-1 topic',
    #         2: '1-1-2 topic',
    #     },
    #     'Subcategory 2 of first category': {
    #         3: '1-2-1 topic',
    #         4: '1-2-2 topic',
    #     },
    # }
    topics_categories = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = _('Your replies')
        context['topics_categories'] = self.topics_categories
        context['statuses'] = m.opinion_statuses_to_display_to_participant

        context['topic_verbose'] = _('Filter by topic')
        context['status_verbose'] = _('Filter by status')
        context['apply_btn'] = _('Apply filters')
        context['reset_btn'] = _('Reset')
        return context

    def get_queryset(self):
        qs = super().get_queryset().order_by('-pk').filter(publisher=self.request.user)

        # QuerySet
        opinions_values = qs.values('id', 'recorded', 'status', 'topic_id', text=F(lang('_text')))
        topics_values = m.Topic.objects.all().values('id', category_name=F('category_id__'+lang('_name')), name=F(lang('_name')))

        # Making object_list & self.topics_categories
        topics_name = {}
        for topic in topics_values:
            topics_name[topic['id']] = topic['name']
            self.topics_categories[topic['category_name']] = {}
        for topic in topics_values:
            self.topics_categories[topic['category_name']][topic['id']] = topic['name']

        opinions = []
        for opinion in opinions_values:
            opinions.append({
                'id': opinion['id'],
                'recorded': opinion['recorded'],
                'status': opinion['status'],
                'verbose_status': m.opinion_verbose_status(opinion['status'], to_display_to_participant=True),
                'topic_id': opinion['topic_id'],
                'topic_name': topics_name[opinion['topic_id']],
                'text': opinion['text'],
            })
        return opinions


@login_required
def your_reply(request, pk):
    l2 = request.user.l2
    if l2:
        opinion_values = get_object_or_404(
            m.Opinion.objects.values(
                'recorded', 'status', 'publisher_id', 'reason_for_rejection', publisher_name=F('publisher_id__name'),
                topic_category_apex_name=F('topic_id__category_id__apex_id__' + lang('_name')),
                topic_category_name=F('topic_id__category_id__' + lang('_name')), topic_name=F('topic_id__' + lang('_name')),
                apex_recorded=F('apex_id__recorded'), apex_publisher_name=F('apex_id__publisher_id__name'),
                apex_text=F('apex_id__' + lang('_text')),
                l1_text=F(lang('_text')), l2_text=F(l2 + '_text'),
            ),
            pk=pk
        )
    else:
        opinion_values = get_object_or_404(
            m.Opinion.objects.values(
                'recorded', 'status', 'publisher_id', 'reason_for_rejection', publisher_name=F('publisher_id__name'),
                topic_category_apex_name=F('topic_id__category_id__apex_id__' + lang('_name')),
                topic_category_name=F('topic_id__category_id__' + lang('_name')), topic_name=F('topic_id__' + lang('_name')),
                apex_recorded=F('apex_id__recorded'), apex_publisher_name=F('apex_id__publisher_id__name'),
                apex_text=F('apex_id__' + lang('_text')),
                l1_text=F(lang('_text')),
            ),
            pk=pk
        )
    if opinion_values['publisher_id'] != request.user.id:
        raise PermissionDenied
    return render(request, 'opinion/your_reply.html', {
        'label': _('Your reply'),
        'opinion_id': pk,
        'l2': l2,
        'opinion': opinion_values,
        'documents': m.OpinionAttachment.objects.filter(opinion_id=pk, deleted=False).values('id', 'document', 'original_label', 'size'),
        'opinion_verbose_status': m.opinion_verbose_status(opinion_values['status'], to_display_to_participant=True),
    })


class Topic(mix.ListViewContextPaginated, ListView):
    model = m.Opinion
    template_name = 'opinion/topic.html'
    topic_values = None
    l2 = None

    def dispatch(self, request, *args, **kwargs):
        self.topic_values = get_object_or_404(
            m.Topic.objects.values(
                'id', category_apex_slug=F('category_id__apex_id__slug'), category_apex_name=F('category_id__apex_id__' + lang('_name')),
                category_slug=F('category_id__slug'), category_name=F('category_id__' + lang('_name')), name=F(lang('_name')),
            ),
            slug=kwargs.get('topic_slug')
        )
        if request.user.is_authenticated:
            self.l2 = request.user.l2
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': self.topic_values['name'],
            'l2': self.l2,
            'topic': self.topic_values,
            'article': get_article_for_context(self.request.user, self.request.META['HTTP_USER_AGENT'], topic_id_only=self.topic_values['id']),
            'jumbotron': get_jumbotron_for_context(self.request.user, topic_id_only=self.topic_values['id']),
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(topic_id=self.topic_values['id'], status=1)
        if self.l2:
            opinions_values = qs.values(
                'id', 'recorded', publisher_name=F('publisher_id__name'), apex_recorded=F('apex_id__recorded'),
                apex_publisher_name=F('apex_id__publisher_id__name'), apex_text=F('apex_id__' + lang('_text')),
                l1_text=F(lang('_text')), l2_text=F(self.l2+'_text'),
            )
        else:
            opinions_values = qs.values(
                'id', 'recorded', publisher_name=F('publisher_id__name'), apex_recorded=F('apex_id__recorded'),
                apex_publisher_name=F('apex_id__publisher_id__name'), apex_text=F('apex_id__' + lang('_text')),
                l1_text=F(lang('_text')),
            )

        # Attachment
        opinions_ids = []
        attachment_dict = {}
        for opinion in opinions_values:
            opinions_ids.append(opinion['id'])
            attachment_dict[opinion['id']] = []
        attachment_values = m.OpinionAttachment.objects.filter(opinion_id__in=opinions_ids, deleted=False)\
            .values('opinion_id', 'document', 'original_label', 'size')
        for attachment in attachment_values:
            attachment_dict[attachment['opinion_id']].append({
                'document': attachment['document'],
                'original_label': attachment['original_label'],
                'size': attachment['size'],
            })

        # Making object_list
        opinions_with_attachment = []
        if self.l2:
            for opinion in opinions_values:
                opinions_with_attachment.append({
                    'id': opinion['id'],
                    'recorded': opinion['recorded'],
                    'publisher_name': opinion['publisher_name'],

                    'apex_recorded': opinion['apex_recorded'],
                    'apex_publisher_name': opinion['apex_publisher_name'],
                    'apex_text': opinion['apex_text'],

                    'l1_text': opinion['l1_text'],
                    'l2_text': opinion['l2_text'],
                    'documents': attachment_dict[opinion['id']],
                })
        else:
            for opinion in opinions_values:
                opinions_with_attachment.append({
                    'id': opinion['id'],
                    'recorded': opinion['recorded'],
                    'publisher_name': opinion['publisher_name'],

                    'apex_recorded': opinion['apex_recorded'],
                    'apex_publisher_name': opinion['apex_publisher_name'],
                    'apex_text': opinion['apex_text'],

                    'l1_text': opinion['l1_text'],
                    'documents': attachment_dict[opinion['id']],
                })
        return opinions_with_attachment
