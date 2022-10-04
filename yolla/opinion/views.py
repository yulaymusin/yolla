from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView
from yolla.common import mixins as mix
from yolla.common.utils import login_and_staff_required
from . import models as m


class FilterByTopicAndStatusMixin:
    topic_id = None
    status_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic_id'] = self.topic_id
        context['status_id'] = self.status_id

        context['topic_verbose'] = 'Filter by topic'
        context['status_verbose'] = 'Filter by status'
        context['apply_btn'] = 'Apply filters'
        context['reset_btn'] = 'Reset'
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        topic = self.request.GET.get('topic')
        try:
            qs = qs.filter(topic=int(topic))
            self.topic_id = int(topic)
        except (TypeError, ValueError):
            pass
        status = self.request.GET.get('status')
        try:
            qs = qs.filter(status=int(status))
            self.status_id = int(status)
        except (TypeError, ValueError):
            pass
        return qs


class List(LoginRequiredMixin, mix.StaffRequiredMixin, mix.ListViewContextPaginated, FilterByTopicAndStatusMixin, ListView):
    model = m.Opinion
    template_name = 'opinion/list.html'
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
        context['label'] = 'Opinions'
        context['topics_categories'] = self.topics_categories
        context['statuses'] = m.opinion_statuses
        return context

    def get_queryset(self):
        qs = super().get_queryset().order_by('-updated')

        # QuerySet
        opinions_values = qs.values('id', 'recorded', 'updated', 'status', 'topic_id', 'en_text', publisher_name=F('publisher_id__name'))
        topics_values = m.Topic.objects.all().values('id', 'en_name', category_en_name=F('category_id__en_name'))

        # Making object_list & self.topics_categories
        topics_en_name = {}
        for topic in topics_values:
            topics_en_name[topic['id']] = topic['en_name']
            self.topics_categories[topic['category_en_name']] = {}
        for topic in topics_values:
            self.topics_categories[topic['category_en_name']][topic['id']] = topic['en_name']

        opinions = []
        for opinion in opinions_values:
            opinions.append({
                'id': opinion['id'],
                'recorded': opinion['recorded'],
                'updated': opinion['updated'],
                'verbose_status': m.opinion_verbose_status(opinion['status']),
                'publisher_name': opinion['publisher_name'],
                'topic_id': opinion['topic_id'],
                'topic_en_name': topics_en_name[opinion['topic_id']],
                'en_text': opinion['en_text'],
            })
        return opinions


class New(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, CreateView):
    model = m.Opinion
    fields = ('status',
              'en_text', 'zh_hans_text', 'es_text', 'ar_text', 'fr_text', 'ru_text')
    template_name = 'opinion/form.html'
    success_message = 'New opinion: done.'
    topic_values = None

    def dispatch(self, request, *args, **kwargs):
        self.topic_values = get_object_or_404(
            m.Topic.objects.values(
                'id', 'slug', 'en_name', category_apex_en_name=F('category_id__apex_id__en_name'), category_en_name=F('category_id__en_name')
            ),
            slug=kwargs.get('topic_slug')
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': 'New opinion',
            'topic': self.topic_values,
        })
        if m.Opinion.objects.filter(topic_id=self.topic_values['id']).count() > 0:
            messages.warning(self.request, 'This topic already have apex opinion.')
        return context

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        form.instance.topic_id = self.topic_values['id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('opinion:read', kwargs={'pk': self.object.id})


class Update(LoginRequiredMixin, mix.StaffRequiredMixin, mix.MsgInFormValid, UpdateView):
    model = m.Opinion
    fields = ('status', 'reason_for_rejection',
              'en_text', 'zh_hans_text', 'es_text', 'ar_text', 'fr_text', 'ru_text')
    template_name = 'opinion/form.html'
    success_url = reverse_lazy('opinion:list')
    success_message = 'Opinion updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_values = get_object_or_404(
            m.Topic.objects.values(
                'id', 'slug', 'en_name', category_apex_en_name=F('category_id__apex_id__en_name'), category_en_name=F('category_id__en_name')
            ),
            pk=self.object.topic_id
        )
        context.update({
            'label': 'Update opinion',
            'topic': topic_values,
            'opinion_id': self.kwargs.get('pk'),
            'documents': m.OpinionAttachment.objects.filter(opinion_id=self.object.pk,
                                                            deleted=False).values('id', 'document', 'original_label', 'size'),
        })
        return context

    def form_valid(self, form):
        if form.cleaned_data.get('status') == 6 and not form.cleaned_data.get('reason_for_rejection'):
            messages.error(self.request, '"Reason for rejection" must be filled in.')
            return super().form_invalid(form)
        if form.cleaned_data.get('status') == 1:
            form.instance.topic.updated = timezone.now()
            form.instance.topic.save(update_fields=('updated',))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('opinion:read', kwargs={'pk': self.kwargs.get('pk')})


@login_and_staff_required
def read(request, pk):
    opinion_values = get_object_or_404(
        m.Opinion.objects.values(
            'recorded', 'updated', 'status', 'reason_for_rejection',
            'en_text', 'zh_hans_text', 'es_text', 'ar_text', 'fr_text', 'ru_text',
            publisher_name=F('publisher_id__name'),
            topic_category_apex_en_name=F('topic_id__category_id__apex_id__en_name'),
            topic_category_en_name=F('topic_id__category_id__en_name'),
            topic_en_name=F('topic_id__en_name'),
            apex_recorded=F('apex_id__recorded'),
            apex_publisher_name=F('apex_id__publisher_id__name'),
            apex_en_text=F('apex_id__en_text'),
        ),
        pk=pk
    )
    return render(request, 'opinion/read.html', {
        'label': 'Read opinion',
        'opinion_id': pk,
        'opinion': opinion_values,
        'opinion_verbose_status': m.opinion_verbose_status(opinion_values['status']),
        'documents': m.OpinionAttachment.objects.filter(opinion_id=pk, deleted=False).values('id', 'document', 'original_label', 'size'),
    })
