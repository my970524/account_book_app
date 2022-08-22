from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AccountBook
from .serializers import AccountBookSerializer


# url : GET, POST /api/v1/account_books
class AccountBookListCreateView(generics.ListCreateAPIView):
    """
    Assignee : 민지

    AccountBook 목록 조회, 생성을 위한 view 입니다.
    """

    permission_classes = [IsAuthenticated]

    queryset = AccountBook.objects.all()
    serializer_class = AccountBookSerializer

    def create(self, request):
        context = {"user": request.user}
        serializer = self.serializer_class(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "게시글 작성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
