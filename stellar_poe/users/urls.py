from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(template_name="login.html", success_url="/"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "change-password",
        auth_views.PasswordChangeView.as_view(
            template_name="users/change_password.html", success_url="/"
        ),
        name="change-password",
    ),
    path("profile", views.UserDetailView.as_view(), name="profile"),
    path("signup", views.SignupView.as_view(), name="signup"),
]
