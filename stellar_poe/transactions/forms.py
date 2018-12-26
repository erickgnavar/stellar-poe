from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from .models import Transaction


User = get_user_model()


class TransactionForm(forms.ModelForm):

    MAX_SIZE = 10_485_760  # 10Mb

    class Meta:
        model = Transaction
        fields = ("recipient", "message", "file")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["recipient"].queryset = User.objects.exclude(id=request.user.id)

    def clean_file(self):
        file_ = self.cleaned_data.get("file")
        if file_ and file_.size < self.MAX_SIZE:
            return file_
        else:
            raise forms.ValidationError(_("File too big, max file size is 10Mb"))
