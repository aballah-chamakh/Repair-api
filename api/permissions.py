from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS :
            return True


        # we gonna add new  bool field of offer called hide
        return obj.profile == request.user.profile_set


class PasswordOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS :
            return True


        # we gonna add new  bool field of offer called hide
        return obj == request.user
