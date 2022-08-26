from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUp, Login, Logout
from .forms import UserPasswordResetForm


urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logot', Logout.as_view(), name='logout'),
    path('account/password_change', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name="password_change"),
    path('account/password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name="password_change_done"),
    path('account/password_reset', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', form_class=UserPasswordResetForm), name="password_reset"),
    path('account/password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]