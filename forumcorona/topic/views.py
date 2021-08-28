from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from forumcorona.common import mixins as mix
from forumcorona.common.utils import lang
from forumcorona.article.models import get_article_for_context
from forumcorona.jumbotron.models import get_jumbotron_for_context
from . import models as m


class List(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ListViewContextPaginated, ListView):
    model = m.Topic
    template_name = 'topic/list.html'
    category_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'Topics'
        context['filter_by_category'] = self.category_id
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('category')
        try:
            if category:
                qs = qs.filter(category=int(category))
                self.category_id = int(category)
        except ValueError:
            pass
        return qs.values('id', 'created', 'updated', 'slug', 'published', 'en_name', category_en_name=F('category_id__en_name'),)


class New(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, CreateView):
    model = m.Topic
    fields = ('slug', 'published', 'category',
              'en_name', 'zh_hans_name', 'es_name', 'ar_name', 'fr_name', 'ru_name',
              'en_description', 'zh_hans_description', 'es_description', 'ar_description', 'fr_description', 'ru_description')
    template_name = 'topic/form.html'
    success_url = reverse_lazy('topic:list')
    success_message = 'New topic: done.'
    extra_context = {
        'label': 'New topic',
    }


class Update(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, UpdateView):
    model = m.Topic
    fields = ('slug', 'published', 'category',
              'en_name', 'zh_hans_name', 'es_name', 'ar_name', 'fr_name', 'ru_name',
              'en_description', 'zh_hans_description', 'es_description', 'ar_description', 'fr_description', 'ru_description')
    template_name = 'topic/form.html'
    success_url = reverse_lazy('topic:list')
    success_message = 'Topic updated.'
    extra_context = {
        'label': 'Update topic',
    }


class Category(mix.ListViewContextPaginated, ListView):
    model = m.Topic
    template_name = 'topic/category.html'
    category_values = None

    def dispatch(self, request, *args, **kwargs):
        self.category_values = get_object_or_404(
            m.Category.objects.values('id', apex_slug=F('apex_id__slug'), apex_name=F('apex_id__'+lang('_name')), name=F(lang('_name')),),
            slug=kwargs.get('category_slug')
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': self.category_values['name'],
            'category': self.category_values,
            'article': get_article_for_context(self.request.user, self.request.META['HTTP_USER_AGENT'],
                                               category_id_only=self.category_values['id']),
            'jumbotron': get_jumbotron_for_context(self.request.user, category_id_only=self.category_values['id']),
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(category_id=self.category_values['id'], published=True)
        return qs.values('slug', name=F(lang('_name')), description=F(lang('_description')),)
