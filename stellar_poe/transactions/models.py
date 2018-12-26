import hashlib
import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Transaction(TimeStampedModel):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Sender"),
        related_name="+",
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Recipient"),
        related_name="+",
    )

    file = models.FileField(_("File"), upload_to="transaction/%Y/%m/%d/")
    file_hash = models.CharField(max_length=32, editable=False)
    stellar_response_data = JSONField(
        _("Stellar transaction response data"), null=True, blank=True
    )
    is_submitted = models.BooleanField(default=False)
    stellar_transaction_link = models.URLField(null=True)
    stellar_transaction_hash = models.CharField(max_length=64, null=True)

    message = models.CharField(_("Message"), max_length=100)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ("-created",)

    def __str__(self):
        return self.message

    def compute_hash_file(self):
        self.file_hash = hashlib.md5(self.file.read()).hexdigest()
