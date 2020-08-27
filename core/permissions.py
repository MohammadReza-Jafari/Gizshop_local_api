from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsBossOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_boss:
            return True
        return request.user == obj.author
