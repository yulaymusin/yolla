import pytz
from django.shortcuts import redirect
from django.utils import timezone, translation


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class TimezoneMiddleware(Middleware):
    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if request.user.is_authenticated is True:
            tzname = request.user.time_zone

        if tzname:
            # if tzname != timezone.get_current_timezone():
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

        return super().__call__(request)


class LanguageMiddleware(Middleware):
    def __call__(self, request):
        lang = translation.get_language()
        if request.user.is_authenticated is True:
            user_l1 = request.user.l1
            if user_l1 != lang:
                return redirect('/' + user_l1 + '/' + request.get_full_path()[1 + len(lang) + 1:])

        return super().__call__(request)
