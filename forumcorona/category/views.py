from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from forumcorona.common import mixins as mix
from forumcorona.common.utils import lang
from forumcorona.topic.models import get_topics_grouped_by_category_id
from forumcorona.article.models import get_article_for_context
from forumcorona.jumbotron.models import get_jumbotron_for_context
from . import models as m


class List(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ListViewContextPaginated, ListView):
    model = m.Category
    template_name = 'category/list.html'
    extra_context = {
        'label': 'Categories',
    }

    def get_queryset(self):
        return super().get_queryset().values('id', 'order_by_this', 'show_in_top_nav', 'en_name', apex_en_name=F('apex_id__en_name'),)


class New(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, CreateView):
    model = m.Category
    fields = ('order_by_this', 'slug', 'apex', 'show_in_top_nav',
              'en_name', 'zh_hans_name', 'zh_hant_name', 'es_name', 'ar_name', 'fr_name', 'ru_name')
    template_name = 'category/form.html'
    success_url = reverse_lazy('category:list')
    success_message = 'New category: done.'
    extra_context = {
        'label': 'New category',
    }


class Update(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, UpdateView):
    model = m.Category
    fields = ('order_by_this', 'slug', 'apex', 'show_in_top_nav',
              'en_name', 'zh_hans_name', 'zh_hant_name', 'es_name', 'ar_name', 'fr_name', 'ru_name')
    template_name = 'category/form.html'
    success_url = reverse_lazy('category:list')
    success_message = 'Category updated.'
    extra_context = {
        'label': 'Update category',
    }


def container(request, slug):
    category_values = get_object_or_404(m.Category.objects.values('id', 'slug', name=F(lang('_name')),), slug=slug, apex=None)
    subcategories_values = m.Category.objects.filter(apex_id=category_values['id']).values('id', 'slug', name=F(lang('_name')),)
    the_subcategories = {}
    categories_of_topics = []
    for subcategory in subcategories_values:
        the_subcategories[subcategory['id']] = subcategory
        categories_of_topics.append(subcategory['id'])
    topics = get_topics_grouped_by_category_id(categories_of_topics, select_limit=10)

    subcategories = {}
    for key, item in the_subcategories.items():
        subcategories[key] = (item, topics[key])

    # categories_topics = {
    #     2: ('Second category', {
    #         6: ('Subcategory 1 of second category', [
    #             'Topic 1 of subcategory 1 of second category',
    #             'Topic 2 of subcategory 1 of second category',
    #             'Topic 3 of subcategory 1 of second category',
    #         ]),
    #         7: ('Subcategory 2 of second category', [...]),
    #     }),
    # }
    categories_topics = {
        category_values['id']: (category_values, subcategories)
    }
    return render(request, 'category/container.html', {
        'label': category_values['name'],
        'categories_topics': categories_topics,
        'article': get_article_for_context(request.user, request.META['HTTP_USER_AGENT'], category_id_only=category_values['id']),
        'jumbotron': get_jumbotron_for_context(request.user, category_id_only=category_values['id']),
    })
