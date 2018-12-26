from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from stellar_poe.stellar import utils

from . import forms
from .models import Transaction


class TransactionCreateView(LoginRequiredMixin, CreateView):

    template_name = "transactions/transaction-create.html"
    model = Transaction
    success_url = reverse_lazy("transactions:transaction-list")
    form_class = forms.TransactionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        # TODO: move this logic to another module
        transaction = form.save(commit=False)
        transaction.sender = self.request.user
        transaction.compute_hash_file()
        response = super().form_valid(form)
        res = utils.create_transaction(
            transaction.sender.stellar_seed,
            transaction.recipient.stellar_key,
            transaction.file_hash,
        )
        transaction.stellar_response_data = res
        transaction.is_submitted = True
        transaction.stellar_transaction_link = res["_links"]["transaction"]["href"]
        transaction.stellar_transaction_hash = res["hash"]
        transaction.save()
        return response


class TransactionListView(LoginRequiredMixin, ListView):

    template_name = "transactions/transaction-list.html"
    model = Transaction
    paginate_by = settings.PAGINATION_DEFAULT_PAGE_SIZE
    context_object_name = "transactions"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
            .select_related("recipient", "sender")
        )


class TransactionDetailView(LoginRequiredMixin, DetailView):

    template_name = "transactions/transaction-detail.html"
    model = Transaction
    context_object_name = "transaction"
    pk_url_kwarg = "id"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
        )
