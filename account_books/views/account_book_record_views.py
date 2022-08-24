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

    # def get_object_and_check_permission(self, account_book_id):
    #     try:
    #         account_book = AccountBook.objects.get(id=account_book_id)
    #     except AccountBook.DoesNotExist:
    #         return

    #     self.check_object_permissions(self.request, account_book)
    #     return account_book

    def create(self, request, pk):
        if request.user.is_anonymous:
            return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        account_book = get_object_or_404(AccountBook, pk=pk, is_deleted=False)

        if account_book.writer != request.user:
            if request.user.is_admin != True:
                return Response({"detail": "이 작업을 수행할 권한(permission)이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        context = {"account_book": account_book}
        serializer = self.serializer_class(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "기록 생성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, pk):
        if request.user.is_anonymous:
            return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        account_book = get_object_or_404(AccountBook, pk=pk, is_deleted=False)

        if request.GET.get("is_deleted"):
            if account_book.writer != request.user:
                if not request.user.is_admin:
                    return Response({"detail": "이 작업을 수행할 권한(permission)이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            queryset = AccountBookRecord.objects.filter(account_book=account_book, is_deleted=True)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if account_book.writer != request.user:
            if not request.user.is_admin:
                return Response({"detail": "이 작업을 수행할 권한(permission)이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        queryset = AccountBookRecord.objects.filter(account_book=account_book, is_deleted=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# url : GET, PUT, PATCH /api/v1/account_books/<account_book_id>/records/<account_book_record_id>
# class AccountBookRetrieveUpdateDeleteView(generics.RetrieveUpdateAPIView):
#     """
#     Assignee : 민지

#     가계부 기록의 상세조회, 수정(PUT), 삭제(PATCH)를 위한 view 입니다.
#     관리자와 가계부 작성자 본인만 사용 가능한 기능입니다.
#     """

#     permission_classes = [IsOwnerOrAuthenticatedCreateOnly]

#     def get_queryset(self):
#         queryset = AccountBookRecord.objects.filter(is_deleted=False, pk=self.kwargs["record_pk"])
#         return queryset

#     serializer_class = AccountBookUpdateSerializer

#     def get_object_and_check_permission(self, record_id):
#         try:
#             account_book_record = AccountBookRecord.objects.get(id=record_id)
#         except AccountBookRecord.DoesNotExist:
#             return

#         self.check_object_permissions(self.request, account_book_record)
#         return account_book_record
