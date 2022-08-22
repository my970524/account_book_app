import json

from django.test import Client, TestCase

from users.models import User

# from .models import AccountBook, AccountBookRecord


class CreateAccountBookTest(TestCase):
    """
    Assignee : 민지

    가계부 생성 기능을 테스트 합니다.
    가계부 생성은 로그인 한 유저만 가능하기 때문에,
    로그인 한 유저와, 로그인 하지 않은 유저의 경우 두 가지를 테스트 합니다.
    """

    url = "/api/v1/account_books"

    def setUp(self):
        self.email = "test1@gmail.com"
        self.username = "test1"
        self.password = "test1"
        self.user_test1 = User.objects.create_user(self.email, self.username, self.password)

    def tearDown(self):
        User.objects.all().delete()

    def test_create_account_book_with_authentication(self):
        """로그인한 유저가 가계부 생성하는 경우를 테스트 합니다."""
        client = Client()
        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, format="json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = {
            "writer": self.user_test1,
            "title": "account_book1",
            "balance": 10000,
        }
        response = client.post(self.url, account_book, format="json", **header)
        self.assertEqual(response.status_code, 201)

    def test_create_account_book_without_authentication(self):
        """로그인 하지 않은 유저가 가계부 생성하는 경우를 테스트 합니다."""
        client = Client()
        account_book = {
            "writer": self.user_test1,
            "title": "account_book1",
            "balance": 10000,
        }
        response = client.post(self.url, account_book, format="json")
        self.assertEqual(response.status_code, 401)
