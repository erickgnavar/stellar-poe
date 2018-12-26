from django import forms
from django.utils.translation import gettext as _

from .models import User


class SignupForm(forms.ModelForm):

    confirm_password = forms.CharField(
        label=_("Confirm password"), widget=forms.PasswordInput, required=True
    )

    class Meta:
        model = User
        fields = ("username", "password", "confirm_password")
        widgets = {"password": forms.PasswordInput}

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(_("Password doesn't match"))
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.is_active = True
        user.set_password(self.cleaned_data.get("password"))
        user.gen_address()
        user.ask_for_initial_balance()
        user.save()
        return user
