import json

# from django.contrib import auth
from django.test import Client, TestCase

from account_books.models import AccountBook, AccountBookRecord
from users.models import User


class CreateAccountBookRecordTest(TestCase):
    """
    Assignee : 민지

    가계부 기록 생성 기능을 테스트 합니다.
    본인이 가계부에만 기록 생성이 가능합니다.
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
        record = {"memo": "식료품", "amount": 15000, "date": "2022-07-08"}
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
        record = {"memo": "식료품", "amount": 15000, "date": "2022-07-08"}
        response = client.post(url, record, content_type="application/json", **header)
        self.assertEqual(response.status_code, 403)


class ListAccountBookRecordTest(TestCase):
    """
    Assignee : 민지

    가계부 기록 목록 조회 기능을 테스트 합니다.
    본인의 가계부 기록들만 조회할 수 있습니다.
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

        self.account_book_record1 = AccountBookRecord.objects.create(
            account_book=self.test1_account_book1,
            memo="간식비",
            amount=-7000,
            date="2022-07-01",
        )

        self.account_book_record2 = AccountBookRecord.objects.create(
            account_book=self.test1_account_book1,
            memo="교통비",
            amount=-4000,
            date="2022-07-01",
            is_deleted=True,
        )

    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        AccountBookRecord.objects.all().delete()

    def test_list_account_book_records(self):
        """본인의 가계부 기록들만 조회 가능한지 테스트 합니다."""

        client = Client()

        sign_in_info_1 = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response_1 = client.post("/api/users/signin", sign_in_info_1, content_type="application/json")
        header_1 = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response_1.content)["access_token"]}'}

        account_book = AccountBook.objects.get(id=1)
        url = f"/api/v1/account_books/{account_book.id}/records"
        response_1 = client.get(url, content_type="application/json", **header_1)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.content.decode().count("memo"), 1)

        sign_in_info_2 = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response_2 = client.post("/api/users/signin", sign_in_info_2, content_type="application/json")
        header_2 = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response_2.content)["access_token"]}'}

        response_2 = client.get(url, content_type="application/json", **header_2)
        self.assertEqual(response_2.status_code, 403)
        self.assertEqual(response_2.content.decode().count("memo"), 0)

    def test_list_deleted_account_book_records_by_owner(self):
        """본인 가계부의 삭제된 기록 목록 조회를 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(id=1)
        url = f"/api/v1/account_books/{account_book.id}/records?is_deleted=true"
        response = client.get(url, content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count("memo"), 1)


class UpdateAccountBookRecordTest(TestCase):
    """
    Assignee : 민지

    가계부 기록 수정 기능을 테스트 합니다.
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

        self.account_book_record1 = AccountBookRecord.objects.create(
            account_book=self.test1_account_book1,
            memo="간식비",
            amount=-7000,
            date="2022-07-01",
        )

    def tearDown(self):
        User.objects.all().delete()
        AccountBook.objects.all().delete()
        AccountBookRecord.objects.all().delete()

    def test_update_account_book_records_by_owner(self):
        """본인 가계부의 기록 수정을 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(id=1)
        account_book_record = AccountBookRecord.objects.get(id=1)

        url = f"/api/v1/account_books/{account_book.id}/records/{account_book_record.id}"

        new_account_book_record_data = {"memo": "교통비"}

        response = client.put(url, new_account_book_record_data, content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("간식비", response.content.decode())
        self.assertIn("교통비", response.content.decode())

    def test_update_account_book_records_by_other(self):
        """다른 사람의 가계부의 기록 수정을 테스트 합니다."""

        client = Client()

        sign_in_info = {
            "email": "test2@gmail.com",
            "password": "test2",
        }
        sign_in_response = client.post("/api/users/signin", sign_in_info, content_type="application/json")
        header = {"HTTP_AUTHORIZATION": f'Bearer {json.loads(sign_in_response.content)["access_token"]}'}

        account_book = AccountBook.objects.get(id=1)
        account_book_record = AccountBookRecord.objects.get(id=1)
        url = f"/api/v1/account_books/{account_book.id}/records/{account_book_record.id}"

        new_account_book_record_data = {"memo": "8월 가계부"}

        response = client.put(url, new_account_book_record_data, content_type="application/json", **header)
        self.assertEqual(response.status_code, 403)
