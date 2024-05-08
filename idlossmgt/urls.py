from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('lost_ids/', lid_view, name='lost_ids'),
    path('success/', success, name='success'),
    path('search-id/', search_id, name='search_id'),
    path('signup/', signup, name='signup'),
    path('lostid/', lostid, name='lostid'),
    path('found_ids/', fid_view, name='found_ids'),
    path('foundid/', foundid, name='foundid'),
    path('confirm_email/<str:uidb64>/<str:token>/', confirm_email, name='confirm_email'),
    path('email_confirmation/', email_confirmation, name='email_confirmation'),
    path('email_confirmed/', email_confirmed, name='email_confirmed'),
    path('email_confirmation_invalid/', email_confirmation_invalid, name='email_confirmation_invalid'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    path('about/', about_us, name='about_us'),
]
