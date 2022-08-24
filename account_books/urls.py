from django.urls import path

from .views.account_book_record_views import AccountBookRecordListCreateView, AccountBookRetrieveUpdateDeleteView
from .views.account_book_views import AccountBookListCreateView, AccountBookRestoreView, AccountBookUpdateDeleteView

urlpatterns = [
    path("", AccountBookListCreateView.as_view(), name="list_create_account_book"),
    path("/<int:pk>", AccountBookUpdateDeleteView.as_view(), name="update_delete_account_book"),
    path("/<int:pk>/restore", AccountBookRestoreView.as_view(), name="restore_account_book"),
    path("/<int:pk>/records", AccountBookRecordListCreateView.as_view(), name="list_create_record"),
    path(
        "/<int:pk>/records/<int:record_pk>",
        AccountBookRetrieveUpdateDeleteView.as_view(),
        name="retrieve_update_delete_record",
    ),
]
