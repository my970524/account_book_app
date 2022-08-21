from django.db import models

from users.models import User


class AccountBook(models.Model):
    """
    Assignee : 민지

    가계부 모델입니다.
    """

    writer = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="account_book")
    title = models.CharField("가계부 제목", max_length=50)
    balance = models.IntegerField("가계부 시작 금액", default=0)
    created_at = models.DateTimeField("생성일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정일자", auto_now=True)
    is_deleted = models.BooleanField("삭제여부", default=False)

    def __str__(self):
        return f"id: {self.pk} / title: {self.title}"


class AccountBookRecord(models.Model):
    """
    Assignee : 민지

    가계부에 기록하는 소득, 소비 기록 모델입니다.
    """

    account_book = models.ForeignKey(
        to=AccountBook, verbose_name="가계부", on_delete=models.CASCADE, related_name="account_book_record"
    )
    date = models.DateField("날짜")
    memo = models.CharField("메모내용", max_length=100)
    amount = models.IntegerField("금액")
    created_at = models.DateTimeField("생성일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정일자", auto_now=True)
    is_deleted = models.BooleanField("삭제여부", default=False)

    def __str__(self):
        return f"id: {self.pk} / memo: {self.memo}"
