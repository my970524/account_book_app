from django.urls import path

from .views import AccountBookListCreateView

urlpatterns = [
    path("", AccountBookListCreateView.as_view(), name="list_create_account_book"),
]
