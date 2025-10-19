"""
权限类定义
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    只允许管理员用户访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    只允许对象所有者或管理员访问
    """
    def has_object_permission(self, request, view, obj):
        # 管理员拥有所有权限
        if request.user.role == 'admin':
            return True
        
        # 检查对象是否有user属性
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # 如果对象本身就是用户
        return obj == request.user
