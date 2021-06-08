from django import template
from forumcorona.category.models import Category
from forumcorona.common.language import lang

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
        # the_categories[category['id']] = category
        the_categories[category['id']] = {
            'id': category['id'],
            'slug': category['slug'],
            'root': category['root'],
            'name': category[lang('_name')],
        }
        categories_pre_tree[category['root']] = {}
    for key, item in the_categories.items():
        categories_pre_tree[item['root']][item['id']] = item
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
    return categories_dict(Category.objects.filter(show_in_top_nav=True).values('id', 'slug', 'root', lang('_name')))


@register.simple_tag
def select_root_in_category_form():
    return categories_dict(Category.objects.filter(root=None).values('id', 'slug', 'root', lang('_name')))


@register.simple_tag
def select_category_in_topic_form():
    return categories_dict(Category.objects.all().values('id', 'slug', 'root', lang('_name')))
