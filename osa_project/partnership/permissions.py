from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated via session
        user_role = request.session.get('user_role')
        return user_role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin or owner
        user_id = request.session.get('user_id')
        user_role = request.session.get('user_role')
        
        if user_role == 'admin':
            return True
        
        # Check if user owns the object
        if hasattr(obj, 'user'):
            return obj.user.user_id == user_id
        
        return False


class IsAuthenticatedViaSession(permissions.BasePermission):
    """
    Custom permission to check if user is authenticated via session.
    """
    def has_permission(self, request, view):
        return 'user_id' in request.session