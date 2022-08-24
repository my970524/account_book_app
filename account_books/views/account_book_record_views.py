from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from account_books.serializers import AccountBookRecordSerializer
from config.permissions import IsOwnerOrAuthenticatedCreateOnly

from ..models import AccountBook, AccountBookRecord


# url : GET, POST /api/v1/account_books/<account_book_id>/records
class AccountBookRecordListCreateView(generics.ListCreateAPIView):
    """
    Assignee : 민지

    AccountBookRecord 목록 조회, 생성을 위한 view 입니다.
    관리자와 가계부 작성자만이 기록의 목록 조회, 생성이 가능합니다.
    """

    permission_classes = [IsOwnerOrAuthenticatedCreateOnly]

    queryset = AccountBookRecord.objects.all()
    serializer_class = AccountBookRecordSerializer

    def create(self, request, pk):
        if request.user.is_anonymous:
            return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        account_book = get_object_or_404(AccountBook, pk=pk, is_deleted=False)

        if account_book.writer != request.user:
            return Response({"detail": "이 작업을 수행할 권한(permission)이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        context = {"account_book": account_book}
        serializer = self.serializer_class(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "기록 생성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
