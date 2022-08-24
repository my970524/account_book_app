from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import AccountBook, AccountBookRecord


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


class AccountBookUpdateSerializer(AccountBookSerializer):
    """
    Assignee : 민지

    AccountBook 수정을 위한 시리얼라이저 입니다.
    """

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.balance = validated_data.get("balance", instance.balance)
        instance.save()

        return instance


class AccountBookDeleteSerializer(AccountBookSerializer):
    """
    Assignee : 민지

    AccountBook 삭제를 위한 시리얼라이저 입니다.
    """

    def update(self, instance, validated_data):
        if instance.is_deleted == True:
            raise serializers.ValidationError("이 가계부는 이미 삭제되었습니다.")
        instance.is_deleted = True
        instance.save()
        return instance

    class Meta:
        model = AccountBook
        exclude = ["id", "writer"]


class AccountBookRestoreSerializer(AccountBookDeleteSerializer):
    """
    Assignee : 민지

    삭제된 가계부 복구를 위한 시리얼라이저 입니다.
    """

    def update(self, instance, validated_data):
        if instance.is_deleted == False:
            raise serializers.ValidationError("이 가계부는 삭제된 가계부가 아닙니다.")
        instance.is_deleted = False
        instance.save()
        return instance


class AccountBookRecordSerializer(ModelSerializer):
    """
    Assignee : 민지

    AccountBookRecord 모델을 위한 시리얼라이저 입니다.
    """

    account_book_title = SerializerMethodField()

    def get_account_book_title(self, obj):
        return obj.account_book.title

    class Meta:
        model = AccountBookRecord
        exclude = ["id", "account_book", "is_deleted"]

    def create(self, validated_data):
        account_book = self.context["account_book"]

        account_book_record = AccountBookRecord.objects.create(account_book=account_book, **validated_data)
        account_book_record.save()

        return account_book_record


class AccountBookRecordUpdateSerializer(AccountBookRecordSerializer):
    """
    Assignee : 민지

    AccountBookRecord 수정을 위한 시리얼라이저 입니다.
    """

    def update(self, instance, validated_data):
        instance.memo = validated_data.get("memo", instance.memo)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.date = validated_data.get("date", instance.date)
        instance.save()

        return instance


class AccountBookRecordDeleteSerializer(AccountBookRecordSerializer):
    """
    Assignee : 민지

    AccountBookRecord 삭제를 위한 시리얼라이저 입니다.
    """

    def update(self, instance, validated_data):
        if instance.is_deleted == True:
            raise serializers.ValidationError("이 가계부는 이미 삭제되었습니다.")
        instance.is_deleted = True
        instance.save()
        return instance

    class Meta:
        model = AccountBookRecord
        exclude = ["id", "account_book"]
