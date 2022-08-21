import json

from django.test import Client, TestCase

from .models import User


class SignUpTest(TestCase):
    """
    Assignee : 민지

    회원가입 기능을 테스트 합니다.
    """

    url = "/api/users/signup"

    def setUp(self):
        self.email = "test1@gmail.com"
        self.username = "test1"
        self.password = "test1"
        self.user_test1 = User.objects.create_user(self.email, self.username, self.password)

    def tearDown(self):
        User.objects.all().delete()

    def test_user_register(self):
        """회원가입으로 새로운 유저 생성을 테스트 합니다."""
        client = Client()
        sign_up_info = {
            "email": "test2@gmail.com",
            "username": "test2",
            "password": "test2",
        }
        response = client.post(self.url, sign_up_info, format="json")
        self.assertEqual(response.status_code, 201)

    def test_unique_email_validation(self):
        """회원가입할 때 이메일 중복을 테스트 합니다."""
        client = Client()
        sign_up_info = {
            "email": "test1@gmail.com",
            "username": "test1",
            "password": "test1",
        }
        response = client.post(self.url, sign_up_info, format="json")
        self.assertEqual(response.status_code, 400)


class SignInViewTest(TestCase):
    """
    Assignee : 민지

    로그인 기능을 테스트 합니다.
    """

    url = "/api/users/signin"

    def setUp(self):
        self.email = "test1@gmail.com"
        self.username = "test1"
        self.password = "test1"
        self.user_test1 = User.objects.create_user(self.email, self.username, self.password)

    def test_signin_success(self):
        """로그인 성공을 테스트 합니다."""
        client = Client()
        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test1",
        }
        response = client.post(self.url, sign_in_info, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", json.loads(response.content))
        self.assertIn("access_token", json.loads(response.content))
        self.assertIn("refresh_token", json.loads(response.content))

    def test_signin_fail_with_wrong_email(self):
        """잘못된 이메일로 로그인 실패를 테스트 합니다."""
        client = Client()
        sign_in_info = {
            "email": "test1@email.com",
            "password": "test1",
        }
        response = client.post(self.url, sign_in_info, format="json")
        self.assertEqual(response.status_code, 401)

    def test_signin_fail_with_wrong_password(self):
        """잘못된 비밀번호로 로그인 실패를 테스트 합니다."""
        client = Client()
        sign_in_info = {
            "email": "test1@gmail.com",
            "password": "test11",
        }
        response = client.post(self.url, sign_in_info, format="json")
        self.assertEqual(response.status_code, 401)
