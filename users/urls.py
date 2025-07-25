from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('subscription/', views.subscription, name='subscription'),
    path('library/', views.library, name='library'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change_form.html',
        success_url='/users/password_change_done/'
    ), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
]
