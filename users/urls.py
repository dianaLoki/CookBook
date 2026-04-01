from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from users.views import LoginUser, RegisterUser, ProfileEditView, ProfileView

app_name = 'users'

urlpatterns = [
    path('login', LoginUser.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('registration', RegisterUser.as_view(), name='registration'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
]