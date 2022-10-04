from django import template
from django.conf import settings
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def languages_settings():
    return settings.LANGUAGES


@register.filter(name='language_in_url')
def language_in_url(the_language_code, url):
    return '/' + the_language_code + '/' + url[1 + len(get_language()) + 1:]


@register.filter(name='language_dir')
def language_dir(the_language_code):
    if the_language_code in settings.RTL_LANGUAGES_CODES:
        return 'rtl'
    return 'ltr'


@register.filter(name='language_from_field_name')
def language_from_field_name(field_name, the_suffix):
    return field_name[:-len(the_suffix)].replace('_', '-')


@register.filter(name='substr_in_str')
def substr_in_str(the_str, the_substr):
    if the_str.find(the_substr) == -1:
        return False
    return True


@register.filter(name='language_dir_form_field')
def language_dir_form_field(field, the_suffix):
    the_language_code = field.name[:-len(the_suffix)].replace('_', '-')
    if the_language_code in settings.RTL_LANGUAGES_CODES:
        return field.as_widget(attrs={'dir': 'rtl', 'lang': the_language_code})
    return field.as_widget(attrs={'dir': 'ltr', 'lang': the_language_code})


@register.filter(name='readable_file_size')
def readable_file_size(size_in_bytes):
    fs_ext = ['Bytes', 'KB', 'MB', 'GB']
    i = 0
    while size_in_bytes > 900:
        size_in_bytes /= 1000
        i += 1
    return str(round((size_in_bytes*100)/100, 1)) + ' ' + fs_ext[i]
