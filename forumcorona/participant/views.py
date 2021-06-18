import pytz
from babel.dates import get_timezone_location
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView, \
    PasswordResetView as BasePasswordResetView, PasswordResetDoneView as BasePasswordResetDoneView, \
    PasswordResetConfirmView as BasePasswordResetConfirmView, PasswordResetCompleteView as BasePasswordResetCompleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import activate, get_language, ugettext_lazy as _
from . import forms as f


def signup(request):
    if request.method == 'POST':
        form = f.SignUpForm(request.POST)
        if form.is_valid():
            form.instance.time_zone = request.POST.get('time_zone') or 'UTC'
            form.instance.l1 = get_language()
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse_lazy('participant:profile'))
    else:
        form = f.SignUpForm()
    return render(request, 'participant/signup.html', {
        'form': form,
        'label': _('Sign up'),
    })


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was changed.'))
            return redirect('participant:password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'participant/form.html', {
        'form': form,
        'label': _('Password change'),
        'btn': _('Change my password'),
        'description': _('Please enter your old password, for security’s sake, and then enter your new password twice '
                         'so we can verify you typed it in correctly.'),
    })


@login_required
def profile(request):
    time_zones = []
    the_lang = get_language().replace('-', '_')
    for tz in pytz.common_timezones_set:
        time_zones.append([tz, get_timezone_location(tz, locale=the_lang)])

    if request.method == 'POST':
        form = f.UserForm(data=request.POST, instance=request.user, time_zones=time_zones)
        if form.is_valid():
            form.save()
            messages.success(request, _('Info and settings saved.'))
            activate(request.user.l1)
            request.session['django_timezone'] = form.instance.time_zone
            return redirect(reverse_lazy('participant:profile'))
    else:
        form = f.UserForm(instance=request.user, time_zones=time_zones)
    return render(request, 'participant/form.html', {'form': form, 'label': _('Profile'), 'btn': _('Save')})


class LoginView(BaseLoginView):
    template_name = 'participant/login.html'
    extra_context = {
        'label': _('Log in'),
    }


class LogoutView(BaseLogoutView):
    template_name = 'participant/logged_out.html'
    extra_context = {
        'label': _('Logged out'),
    }


class PasswordResetView(BasePasswordResetView):
    email_template_name = 'participant/password_reset_email.html'
    success_url = reverse_lazy('participant:password_reset_done')
    template_name = 'participant/password_reset_form.html'
    extra_context = {
        'label': _('Password reset'),
    }
    extra_email_context = {
        'protocol': settings.PROTOCOL,
        'domain': settings.DOMAIN,
        'site_name': settings.SITE_NAME,
    }


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'participant/password_reset_done.html'
    extra_context = {
        'label': _('Password reset'),
    }


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('participant:password_reset_complete')
    template_name = 'participant/password_reset_confirm.html'
    extra_context = {
        'label': _('Password reset confirmation'),
    }


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = 'participant/password_reset_complete.html'
    extra_context = {
        'label': _('Password reset'),
    }
