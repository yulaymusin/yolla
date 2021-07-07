from django import template
from django.db.models import F
from forumcorona.category.models import Category
from forumcorona.common.utils import lang

register = template.Library()


def categories_dict(categories_values):
    if not categories_values:
        return {}
    # categories = {
    #     1: ('First category', {
    #         3: ('Subcategory 1 of first category', {}),
    #         4: ('Subcategory 2 of first category', {}),
    #     }),
    #     2: ('Second category', {}),
    # }
    the_categories = {}
    categories_pre_tree = {}
    for category in categories_values:
        the_categories[category['id']] = category
        categories_pre_tree[category['apex']] = {}
    for key, item in the_categories.items():
        categories_pre_tree[item['apex']][item['id']] = item
    categories = {}
    for key1, item1 in categories_pre_tree[None].items():
        subcategory = {}
        try:
            for key2, item2 in categories_pre_tree[key1].items():
                subcategory[key2] = (item2, {})
        except KeyError:
            pass
        categories[key1] = (item1, subcategory)
    return categories


@register.simple_tag
def categories_for_top_nav():
    return categories_dict(Category.objects.filter(show_in_top_nav=True).values('id', 'slug', 'apex', name=F(lang('_name')),))


@register.simple_tag
def select_apex_in_form():
    return categories_dict(Category.objects.filter(apex=None).values('id', 'slug', 'apex', name=F('en_name'),))


@register.simple_tag
def select_category_in_other_apps_form():
    return categories_dict(Category.objects.all().values('id', 'slug', 'apex', name=F('en_name'),))
