# Generated by Django 4.1 on 2022-08-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("email", models.EmailField(max_length=320, unique=True, verbose_name="이메일")),
                ("username", models.CharField(max_length=200, verbose_name="유저이름")),
                ("password", models.CharField(max_length=100, verbose_name="비밀번호")),
                ("date_joined", models.DateTimeField(auto_now_add=True, verbose_name="가입일자")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일자")),
                ("is_admin", models.BooleanField(default=True, verbose_name="관리자여부")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
