from rest_framework import permissions

MY_BLOCK_LIST = ['1.2.3.4']

class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """
 
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        # blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        blocked = ip_addr in MY_BLOCK_LIST
        return not blocked

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    """
    Permission check for staff users.
    """

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
            # if user.has_perm('user.can_edit_user'):
            #     return True
        return False

    def has_obj_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
        