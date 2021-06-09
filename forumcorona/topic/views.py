from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from forumcorona.common import mixins as mix
from forumcorona.common.language import lang
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
        return qs.select_related('category')


class New(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ContextForGenericView, mix.MsgInFormValid, CreateView):
    model = m.Topic
    fields = ('slug', 'published', 'category',
              'en_name', 'zh_hans_name', 'zh_hant_name', 'es_name', 'ar_name', 'fr_name', 'ru_name',
              'en_description', 'zh_hans_description', 'zh_hant_description', 'es_description', 'ar_description',
              'fr_description', 'ru_description')
    template_name = 'topic/form.html'
    success_url = reverse_lazy('topic:list')
    success_message = 'New topic: done.'
    context = {
        'label': 'New topic',
    }


class Edit(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ContextForGenericView, mix.MsgInFormValid, UpdateView):
    model = m.Topic
    fields = ('slug', 'published', 'category',
              'en_name', 'zh_hans_name', 'zh_hant_name', 'es_name', 'ar_name', 'fr_name', 'ru_name',
              'en_description', 'zh_hans_description', 'zh_hant_description', 'es_description', 'ar_description',
              'fr_description', 'ru_description')
    template_name = 'topic/form.html'
    success_url = reverse_lazy('topic:list')
    success_message = 'Topic edited.'
    context = {
        'label': 'Edit topic',
    }


class Category(mix.ListViewContextPaginated, ListView):
    model = m.Topic
    template_name = 'topic/category.html'
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(m.Category, slug=kwargs.get('category_slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': eval('self.category.' + lang('_name')),
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category=self.category, published=True).values('slug', lang('_name'), lang('_description'))
