from rest_framework import permissions

class IsProcductOwnerOrReadOnly(permissions.BasePermission):
    """
    Special permission for photo api
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print(request.user)
        print(obj.product.owner)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.product.owner == request.user
        

# class IsProcductOwnerOrReadOnly(permissions.BasePermission):
#     """
#     The request is authenticated as a user, and the user is the one who create product.
#     """

#     def has_permission(self, request, view):
#         print(request.user)
#         # get obj owner
#         obj = view.get_object()
#         print(obj.owner)

        
#         return bool(
#             request.method in SAFE_METHODS or
#             request.user and
#             request.user.is_authenticated
#         )
