from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from yolla.common.utils import lang
from yolla.category.models import Category
from yolla.topic.models import get_topics_grouped_by_category_id
from yolla.article.models import get_article_for_context
from yolla.jumbotron.models import get_jumbotron_for_context


def categories_with_topics(request):
    categories_values = Category.objects.all().values('id', 'slug', 'apex', lang('_name'))
    # categories_topics = {
    #     1: ('First category', {
    #         3: ('Subcategory 1 of first category', [
    #             'Topic 1 of subcategory 1 of first category',
    #             'Topic 2 of subcategory 1 of first category',
    #             'Topic 3 of subcategory 1 of first category',
    #         ]),
    #         4: ('Subcategory 2 of first category', [...]),
    #     }),
    #     2: ('Second category', {...}),
    # }
    categories_topics = {}
    if categories_values:
        the_categories = {}
        categories_pre_tree = {}
        for category in categories_values:
            the_categories[category['id']] = {
                'id': category['id'],
                'slug': category['slug'],
                'apex': category['apex'],
                'name': category[lang('_name')],
            }
            categories_pre_tree[category['apex']] = {}
        for key, item in the_categories.items():
            categories_pre_tree[item['apex']][item['id']] = item

        categories_of_topics = []
        for key1, item1 in categories_pre_tree[None].items():
            try:
                for key2, item2 in categories_pre_tree[key1].items():
                    categories_of_topics.append(key2)
            except KeyError:
                pass  # (key1, item1): categories with apex=None

        topics = get_topics_grouped_by_category_id(categories_of_topics)

        for key1, item1 in categories_pre_tree[None].items():
            subcategory = {}
            try:
                for key2, item2 in categories_pre_tree[key1].items():
                    subcategory[key2] = (item2, topics[key2])
            except KeyError:
                pass  # (key1, item1): categories with apex=None
            categories_topics[key1] = (item1, subcategory)
    return render(request, 'common/page_home.html', {
        'label': 'Yolla',
        'h1': _('Important discussions'),
        'categories_topics': categories_topics,
        'page_home': True,
        'article': get_article_for_context(request.user, request.META['HTTP_USER_AGENT']),
        'jumbotron': get_jumbotron_for_context(request.user),
        'more_topics': _('more topics'),
    })
