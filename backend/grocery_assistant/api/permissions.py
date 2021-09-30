from rest_framework import permissions


class AnonRegister(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST' or request.user.is_authenticated


class PermissonForRole(permissions.BasePermission):

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
