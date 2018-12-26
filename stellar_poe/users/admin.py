from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext as _

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update(
        {"duplicate_username": "This username has already been taken."}
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages["duplicate_username"])


def gen_address(modeladmin, request, queryset):
    for user in queryset:
        user.gen_address()
        user.save()


def ask_for_initial_balance(modeladmin, request, queryset):
    for user in queryset:
        result, message = user.ask_for_initial_balance()
        if result:
            messages.success(request, _("Initial balance fetched"))
        else:
            messages.warning(request, message)


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):

    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ("username", "is_superuser", "stellar_key")
    search_fields = ["username"]
    fieldsets = AuthUserAdmin.fieldsets + (("Extra data", {"fields": tuple()}),)
    readonly_fields = ("date_joined", "last_login")
    actions = [gen_address, ask_for_initial_balance]
