from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from stellar_poe.stellar import utils


class User(AbstractUser):

    stellar_seed = models.CharField(
        _("Stellar seed"), max_length=100, null=True, blank=True
    )
    stellar_key = models.CharField(
        _("Stellar key"), max_length=100, null=True, blank=True
    )

    class Meta:
        db_table = "auth_user"

    def gen_address(self):
        self.stellar_seed, self.stellar_key = utils.create_new_address()

    def ask_for_initial_balance(self):
        return utils.ask_for_coins(self.stellar_key)
