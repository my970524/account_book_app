from rest_framework.permissions import BasePermission


class IsOwnerOrAuthenticatedCreateOnly(BasePermission):
    """
    Assignee : 민지

    POST 메소드의 경우, 로그인한 유저 모두 권한을 가집니다.
    이외의 메소드인 경우, 객체의 주인만 권한을 가집니다.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            if request.user.is_authenticated:
                return True
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            elif hasattr(obj, "writer"):
                return obj.writer == request.user
            elif hasattr(obj, "account_book"):
                return obj.account_book.writer == request.user
            return False
        return False
