from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from . import forms
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):

    template_name = "users/profile.html"
    model = User
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class SignupView(CreateView):

    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("home")
