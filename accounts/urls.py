from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
    path('profile-detail/', views.ProfileDetailView.as_view(), name="profile_detail"),
    path('profile-edit/', views.ProfileUpdateView.as_view(), name="profile_edit"),
    path("password-change/",auth_views.PasswordChangeView.as_view(
        template_name = "accounts/password_change_form.html",
        success_url = "done/"
    ), name="password_change",  ), 
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name = "accounts/password_change_done.html",
    ), name="password_change_done", ),
]
