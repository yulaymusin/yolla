from django.urls import path
from . import views as v

app_name = 'participant'

urlpatterns = [
    path('signup', v.signup, name='signup'),  # public
    path('password', v.password, name='password'),  # participant
    path('profile', v.profile, name='profile'),  # participant

    path('login', v.LoginView.as_view(), name='login'),  # public
    path('logout', v.LogoutView.as_view(), name='logout'),  # public
    path('password_reset', v.PasswordResetView.as_view(), name='password_reset'),  # public
    path('password_reset/done', v.PasswordResetDoneView.as_view(), name='password_reset_done'),  # public
    path('reset/<uidb64>/<token>', v.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # public
    path('reset/done', v.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # public
]
