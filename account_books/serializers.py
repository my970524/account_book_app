from rest_framework.serializers import ModelSerializer

from .models import AccountBook


class AccountBookSerializer(ModelSerializer):
    """
    Assignee : 민지

    AccountBook 모델을 위한 시리얼라이저 입니다.
    가계부 생성의 경우 작성자는 로그인한 유저의 정보를 사용하기 때문에,
    create 메소드에서 context를 통해 유저 정보를 가져옵니다.
    """

    class Meta:
        model = AccountBook
        exclude = ["id", "writer", "is_deleted"]

    def create(self, validated_data):
        writer = self.context["user"]

        account_book = AccountBook.objects.create(writer=writer, **validated_data)
        account_book.save()

        return account_book