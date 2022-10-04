from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from yolla.common import mixins as mix
from yolla.common.utils import login_and_superuser_required
from . import models as m


class List(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ListViewContextPaginated, ListView):
    model = m.Jumbotron
    template_name = 'jumbotron/list.html'
    extra_context = {
        'label': 'Jumbotrons',
    }

    def get_queryset(self):
        qs = super().get_queryset()
        jumbotrons_values = qs.values('id', 'page_home', 'en_content', category_en_name=F('category_id__en_name'),
                                      topic_en_name=F('topic_id__en_name'),)
        jumbotrons = []
        for jumbotron in jumbotrons_values:
            jumbotrons.append({
                'id': jumbotron['id'],
                'page_home': jumbotron['page_home'],
                'category_en_name': jumbotron['category_en_name'],
                'topic_en_name': jumbotron['topic_en_name'],
                'en_content': jumbotron['en_content'],
            })
        return jumbotrons


class New(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, mix.TopicsCategoriesContext, CreateView):
    model = m.Jumbotron
    fields = ('page_home', 'category', 'topic',
              'en_content', 'zh_hans_content', 'es_content', 'ar_content', 'fr_content', 'ru_content',)
    template_name = 'common/form_article_jumbotron.html'
    success_message = 'New jumbotron: done.'
    extra_context = {
        'label': 'New jumbotron',
    }

    def get_success_url(self):
        return reverse_lazy('jumbotron:read', kwargs={'pk': self.object.id})


class Update(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, mix.TopicsCategoriesContext, UpdateView):
    model = m.Jumbotron
    fields = ('page_home', 'category', 'topic',
              'en_content', 'zh_hans_content', 'es_content', 'ar_content', 'fr_content', 'ru_content',)
    template_name = 'common/form_article_jumbotron.html'
    success_message = 'Jumbotron updated.'
    extra_context = {
        'label': 'Update jumbotron',
    }

    def get_success_url(self):
        return reverse_lazy('jumbotron:read', kwargs={'pk': self.kwargs.get('pk')})


@login_and_superuser_required
def read(request, pk):
    jumbotron_values = get_object_or_404(
        m.Jumbotron.objects.values(
            'page_home',
            'en_content', 'zh_hans_content', 'es_content', 'ar_content', 'fr_content', 'ru_content',
            category_en_name=F('category_id__en_name'), topic_en_name=F('topic_id__en_name'),
        ),
        pk=pk
    )
    return render(request, 'jumbotron/read.html', {
        'label': 'Read jumbotron',
        'jumbotron_id': pk,
        'jumbotron': jumbotron_values,
    })
