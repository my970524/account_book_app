from django.urls import path

from .views import AccountBookListCreateView, AccountBookRestoreView, AccountBookUpdateDeleteView

urlpatterns = [
    path("", AccountBookListCreateView.as_view(), name="list_create_account_book"),
    path("/<int:pk>", AccountBookUpdateDeleteView.as_view(), name="update_delete_account_book"),
    path("/<int:pk>/restore", AccountBookRestoreView.as_view(), name="restore_account_book"),
]
