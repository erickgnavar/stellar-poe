from django.urls import path

from . import views

app_name = "transactions"


urlpatterns = [
    path("transactions/", views.TransactionListView.as_view(), name="transaction-list"),
    path(
        "transactions/create/",
        views.TransactionCreateView.as_view(),
        name="transaction-create",
    ),
    path(
        "transactions/<uuid:id>/",
        views.TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
]
