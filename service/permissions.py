from rest_framework import permissions

class OwnerOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        return obj.customer_object.service_advisor==request.user