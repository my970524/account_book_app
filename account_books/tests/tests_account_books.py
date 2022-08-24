import json

from django.contrib import auth
from django.test import Client, TestCase

from account_books.models import AccountBook
from users.models import User


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
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = {
            "title": "account_book1",
            "balance": 10000,
        }
        response = client.post(self.url, account_book, content_type="application/json", **header)
        self.assertEqual(response.status_code, 201)

    def test_create_account_book_without_authentication(self):
        """로그인 하지 않은 유저가 가계부 생성하는 경우를 테스트 합니다."""

        client = Client()

        user = auth.get_user(client)
        self.assertEqual(user.is_anonymous, True)

        account_book = {
            "title": "account_book1",
            "balance": 10000,
        }

        response = client.post(self.url, account_book, content_type="application/json")
        self.assertEqual(response.status_code, 401)


class ListAccountBookTest(TestCase):
    """
    Assignee : 민지

    가계부 목록 조회 기능을 테스트 합니다.
    가계부 목록 조회는 로그인 한 유저만 가능하고,
    본인이 작성한 가계부만 조회 가능합니다.
    """

    url = "/api/v1/account_books"

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

        self.test1_account_book2 = AccountBook.objects.create(
            writer=self.user_test1,
            title="8월 가계부",
            balance=400000,
            is_deleted=True,
        )

    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()

    def test_list_account_books(self):
        """본인의 가계부 목록을 조회를 테스트 합니다."""

        client = Client()

        sign_in_info_1 = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response_1 = client.post("/api/users/signin", sign_in_info_1, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response_1.content)["access_token"]}'}
        response_1 = client.get(self.url, content_type="application/json", **header)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.content.decode().count("title"), 1)

        sign_in_info_2 = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response_2 = client.post("/api/users/signin", sign_in_info_2, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response_2.content)["access_token"]}'}
        response_2 = client.get(self.url, content_type="application/json", **header)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.content.decode().count("title"), 0)

    def test_list_deleted_account_books(self):
        """삭제된 가계부 목록 조회를 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}
        response = client.get(self.url + "?is_deleted=true", content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count("title"), 1)


class UpdateDeleteAccountBookTest(TestCase):
    """
    Assignee : 민지

    가계부 수정과 삭제 기능을 테스트 합니다.
    관리자와 작성자 본인만 수정 가능합니다.
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

    def test_update_account_books_by_owner(self):
        """본인의 가계부 수정을 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(title="7월 가계부")
        url = f"/api/v1/account_books/{account_book.id}"

        new_account_book_data = {"balance": 300000}

        response = self.client.put(url, new_account_book_data, content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(response.content.decode(), "200000")

    def test_update_account_books_by_other(self):
        """다른 사람의 가계부 수정을 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(title="7월 가계부")
        url = f"/api/v1/account_books/{account_book.id}"

        new_account_book_data = {"balance": 300000}
        response = self.client.put(url, new_account_book_data, content_type="application/json", **header)
        self.assertEqual(response.status_code, 403)

    def test_delete_account_book_by_owner(self):
        """본인의 가계부 삭제를 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(title="7월 가계부")
        url = f"/api/v1/account_books/{account_book.id}"
        # print(AccountBook.objects.get(title="7월 가계부").is_deleted)
        # print(account_book.is_deleted)
        # print(self.test1_account_book1.is_deleted)
        response = self.client.patch(url, content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(account_book.is_deleted, True)
        # print(AccountBook.objects.get(title="7월 가계부").is_deleted)
        # print(account_book.is_deleted)
        # print(self.test1_account_book1.is_deleted)
        # print(account_book==AccountBook.objects.get(title="7월 가계부"))
        # print(account_book==self.test1_account_book1)
        self.assertEqual(AccountBook.objects.get(title="7월 가계부").is_deleted, True)

    def test_delete_account_book_by_other(self):
        """다른 사람의 가계부 삭제를 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(title="7월 가계부")
        url = f"/api/v1/account_books/{account_book.id}"

        response = self.client.patch(url, content_type="application/json", **header)
        self.assertEqual(response.status_code, 403)


class RestoreAccountBookTest(TestCase):
    """
    Assignee : 민지

    삭제된 가계부 복구 기능을 테스트 합니다.
    관리자와 작성자 본인만 복구 가능합니다.
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
            is_deleted=True,
        )

    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()

    def test_restore_account_book_by_owner(self):
        """본인의 삭제된 가계부 복구를 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(title="7월 가계부")
        url = f"/api/v1/account_books/{account_book.id}/restore"

        response = self.client.patch(url, content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AccountBook.objects.get(title="7월 가계부").is_deleted, False)

    def test_restore_account_book_by_other(self):
        """다른 사람의 삭제된 가계부 복구를 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(title="7월 가계부")
        url = f"/api/v1/account_books/{account_book.id}/restore"

        response = self.client.patch(url, content_type="application/json", **header)
        self.assertEqual(response.status_code, 403)
