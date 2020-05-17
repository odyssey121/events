from rest_framework import permissions


class IsAuthorOfEvents(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, event):
        if request.user:
            return request.user == event.author
        return False