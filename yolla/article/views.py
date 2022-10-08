from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from yolla.common import mixins as mix
from yolla.common.utils import login_and_superuser_required
from . import models as m


class List(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ListViewContextPaginated, ListView):
    model = m.Article
    template_name = 'article/list.html'
    extra_context = {
        'label': 'Articles',
    }

    def get_queryset(self):
        qs = super().get_queryset()
        articles_values = qs.values('id', 'mobile', 'status', 'page_home', 'en_content', category_en_name=F('category_id__en_name'),
                                    topic_en_name=F('topic_id__en_name'),)
        articles = []
        for article in articles_values:
            articles.append({
                'id': article['id'],
                'mobile': article['mobile'],
                'verbose_status': m.article_verbose_status(article['status']),
                'page_home': article['page_home'],
                'category_en_name': article['category_en_name'],
                'topic_en_name': article['topic_en_name'],
                'en_content': article['en_content'],
            })
        return articles


class New(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, mix.TopicsCategoriesContext, CreateView):
    model = m.Article
    fields = ('mobile', 'status', 'page_home', 'category', 'topic',
              'en_content', 'zh_hans_content', 'es_content', 'ar_content', 'fr_content', 'ru_content')
    template_name = 'common/form_article_jumbotron.html'
    success_message = 'New article: done.'
    extra_context = {
        'label': 'New article',
    }

    def get_success_url(self):
        return reverse_lazy('article:read', kwargs={'pk': self.object.id})


class Update(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, mix.TopicsCategoriesContext, UpdateView):
    model = m.Article
    fields = ('mobile', 'status', 'page_home', 'category', 'topic',
              'en_content', 'zh_hans_content', 'es_content', 'ar_content', 'fr_content', 'ru_content')
    template_name = 'common/form_article_jumbotron.html'
    success_message = 'Article updated.'
    extra_context = {
        'label': 'Update article',
    }

    def get_success_url(self):
        return reverse_lazy('article:read', kwargs={'pk': self.kwargs.get('pk')})


@login_and_superuser_required
def read(request, pk):
    article_values = get_object_or_404(
        m.Article.objects.values(
            'mobile', 'status', 'page_home',
            'en_content', 'zh_hans_content', 'es_content', 'ar_content', 'fr_content', 'ru_content',
            category_en_name=F('category_id__en_name'), topic_en_name=F('topic_id__en_name'),
        ),
        pk=pk
    )
    return render(request, 'article/read.html', {
        'label': 'Read article',
        'article_id': pk,
        'article': {
            'mobile': article_values['mobile'],
            'page_home': article_values['page_home'],
            'category_en_name': article_values['category_en_name'],
            'topic_en_name': article_values['topic_en_name'],

            'en_content': m.media_url_in_str(article_values['en_content']),
            'zh_hans_content': m.media_url_in_str(article_values['zh_hans_content']),
            'es_content': m.media_url_in_str(article_values['es_content']),
            'ar_content': m.media_url_in_str(article_values['ar_content']),
            'fr_content': m.media_url_in_str(article_values['fr_content']),
            'ru_content': m.media_url_in_str(article_values['ru_content']),
        },
        'article_verbose_status': m.article_verbose_status(article_values['status']),
    })
