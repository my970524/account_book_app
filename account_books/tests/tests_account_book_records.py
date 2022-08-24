import json

# from django.contrib import auth
from django.test import Client, TestCase

from account_books.models import AccountBook
from users.models import User


class CreateAccountBookRecordTest(TestCase):
    """
    Assignee : 민지

    가계부 기록 생성 기능을 테스트 합니다.
    """

    def setUp(self):
        self.user_test1 = User.objects.create_user(
            email="test1@gmail.com",
            username="test1",
            password="test1",
        )
        self.user_test2 = User.objects.create_user(
            email="test2@gmail.com",
            username="test2",
            password="test2",
        )

        self.test1_account_book1 = AccountBook.objects.create(
            writer=self.user_test1,
            title="7월 가계부",
            balance=200000,
        )

    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()

    def test_create_account_book_record_by_owner(self):
        """본인의 가계부에 기록 생성을 테스트합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(id=1)
        url = f"/api/v1/account_books/{account_book.id}/records"
        record = {"memo": "식료품", "amount": 15000}
        response = client.post(url, record, content_type="application/json", **header)
        self.assertEqual(response.status_code, 201)

    def test_create_account_book_record_by_other(self):
        """다른 사람의 가계부에 기록 생성을 테스트합니다."""

        client = Client()

        sign_in_info = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(id=1)
        url = f"/api/v1/account_books/{account_book.id}/records"
        record = {"memo": "식료품", "amount": 15000}
        response = client.post(url, record, content_type="application/json", **header)
        self.assertEqual(response.status_code, 403)
