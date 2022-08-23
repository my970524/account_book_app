from rest_framework import generics, status
from rest_framework.response import Response

from config.permissions import IsOwnerOrAuthenticatedCreateOnly

from .models import AccountBook
from .serializers import AccountBookSerializer


# url : GET, POST /api/v1/account_books
class AccountBookListCreateView(generics.ListCreateAPIView):
    """
    Assignee : 민지

    AccountBook 목록 조회, 생성을 위한 view 입니다.
    가계부 생성은 로그인 한 유저만 가능합니다.
    가계부 목록 조회는 작성자 본인만 가능합니다.
    """

    permission_classes = [IsOwnerOrAuthenticatedCreateOnly]

    queryset = AccountBook.objects.all()
    serializer_class = AccountBookSerializer

    def create(self, request):
        if request.user.is_anonymous:
            return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        context = {"user": request.user}
        serializer = self.serializer_class(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "가계부 생성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """쿼리 파라미터로 is_deleted=true가 있는 경우,삭제된 가계부 목록을 보여줍니다."""

        if request.GET.get("is_deleted"):
            if request.user.is_anonymous:
                return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
            queryset = AccountBook.objects.filter(writer=request.user, is_deleted=True)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = AccountBook.objects.filter(writer=request.user, is_deleted=False)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
