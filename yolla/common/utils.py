import hashlib
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.translation import get_language


def lang(name_field):
    the_lang = get_language().replace('-', '_')
    return the_lang + name_field


def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def login_and_superuser_required(function):
    """
    Decorator for views
    """
    def check_is_authenticated_and_is_superuser(user):
        if user.is_authenticated and user.is_superuser:
            return True
        if user.is_authenticated and user.is_superuser is False:
            raise PermissionDenied
        return False
    actual_decorator = user_passes_test(check_is_authenticated_and_is_superuser)
    return actual_decorator(function)


def login_and_staff_required(function):
    """
    Decorator for views
    """
    def check_is_authenticated_and_is_staff(user):
        if user.is_authenticated and user.is_staff:
            return True
        if user.is_authenticated and user.is_staff is False:
            raise PermissionDenied
        return False
    actual_decorator = user_passes_test(check_is_authenticated_and_is_staff)
    return actual_decorator(function)
