# Generated by Django 4.1 on 2022-08-24 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(default=False, verbose_name="관리자여부"),
        ),
    ]
