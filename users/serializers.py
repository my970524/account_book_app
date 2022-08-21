from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """
    Assignee : 민지

    회원가입 시리얼라이저 입니다.
    """

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password")

        user = User(
            email=email,
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save()

        return user
