from rest_framework.permissions import BasePermission, SAFE_METHODS

# Permissions for CMS API - only users with user.is_staff will have permission to access API
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff