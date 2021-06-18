from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from forumcorona.common import mixins as mix
from forumcorona.common.language import lang
from forumcorona.topic.models import get_topics_grouped_by_category_id
from . import models as m


class List(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.ListViewContextPaginated, ListView):
    model = m.Category
    template_name = 'category/list.html'
    extra_context = {
        'label': 'Categories',
    }

    def get_queryset(self):
        return super().get_queryset().select_related('apex')


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


class Edit(LoginRequiredMixin, mix.SuperUserRequiredMixin, mix.MsgInFormValid, UpdateView):
    model = m.Category
    fields = ('order_by_this', 'slug', 'apex', 'show_in_top_nav',
              'en_name', 'zh_hans_name', 'zh_hant_name', 'es_name', 'ar_name', 'fr_name', 'ru_name')
    template_name = 'category/form.html'
    success_url = reverse_lazy('category:list')
    success_message = 'Category edited.'
    extra_context = {
        'label': 'Edit category',
    }


def container(request, slug):
    category = get_object_or_404(m.Category, slug=slug, apex=None)
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
    category_dict = {
        'id': category.id,
        'slug': category.slug,
        'apex': category.apex,
        'name': eval('category.' + lang('_name')),
    }
    subcategories_values = m.Category.objects.filter(apex=category).values('id', 'slug', lang('_name'))
    the_subcategories = {}
    categories_of_topics = []
    for subcategory in subcategories_values:
        # the_subcategories[subcategory['id']] = subcategory
        the_subcategories[subcategory['id']] = {
            'id': subcategory['id'],
            'slug': subcategory['slug'],
            'name': subcategory[lang('_name')],
        }
        categories_of_topics.append(subcategory['id'])
    topics = get_topics_grouped_by_category_id(categories_of_topics, select_limit=10)

    subcategories = {}
    for key, item in the_subcategories.items():
        subcategories[key] = (item, topics[key])

    categories_topics = {
        category_dict['id']: (category_dict, subcategories)
    }
    return render(request, 'category/container.html', {
        'categories_topics': categories_topics,
        'label': category_dict['name'],
    })
