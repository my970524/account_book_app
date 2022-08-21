from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer


#  url : POST /api/users/signup
class SignUpView(APIView):
    """
    Assignee : 민지

    회원가입 view 입니다.
    """

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 성공적으로 되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": "회원가입에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
