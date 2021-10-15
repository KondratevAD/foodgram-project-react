from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
        )


class PermissonForRole(BasePermission):
    def __init__(self, roles_permissions) -> None:
        super().__init__()
        self.roles_permissions = roles_permissions

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in self.roles_permissions[request.user.role]
            )
        return request.method in self.roles_permissions['anon']

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in self.roles_permissions[request.user.role]
            )
        return request.method in self.roles_permissions['anon']
