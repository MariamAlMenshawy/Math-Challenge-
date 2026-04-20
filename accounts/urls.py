from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',views.logOut,name='logout'),
    path('profileInfo/',views.UpdateProfileInfo.as_view(),name='profile_info'),
    path('change_passsword/',auth_views.PasswordChangeView.as_view(template_name='change_password.html'),name='change_password'),
    path('change_passsword/done/',auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),name='password_change_done'),

]