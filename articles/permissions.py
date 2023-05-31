from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    SAFE_METHODS = ('GET', )
    message = "접근 권한이 없습니다."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:  # 로그인하지 않은 사용자라면
            if request.method in SAFE_METHODS:  # 읽기만 허용
                return True
            else:
                return False

        if request.user.is_admin or request.method in SAFE_METHODS:
            return True

        return False
