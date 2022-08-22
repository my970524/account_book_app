from rest_framework.serializers import ModelSerializer

from .models import AccountBook


class AccountBookSerializer(ModelSerializer):
    class Meta:
        model = AccountBook
        exclude = ["id", "writer", "is_deleted"]

    def create(self, validated_data):
        writer = self.context["user"]

        account_book = AccountBook.objects.create(writer=writer, **validated_data)
        account_book.save()

        return account_book
