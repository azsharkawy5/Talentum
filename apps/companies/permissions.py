from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManagerUser(permissions.BasePermission):
    """
    Allow access only to manager users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']


class IsEmployeeUser(permissions.BasePermission):
    """
    Allow access only to authenticated users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsOwnerOrManager(permissions.BasePermission):
    """
    Allow access to object owner or managers/admins.
    """
    def has_object_permission(self, request, view, obj):
        # Admin and managers have full access
        if request.user.role in ['admin', 'manager']:
            return True
        
        # Check if user is the owner of the object
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # For employees, check if they own the employee profile
        if hasattr(obj, 'employee_profile') and obj.employee_profile.user == request.user:
            return True
        
        return False


class CompanyPermission(permissions.BasePermission):
    """
    Company permissions:
    - Admin: Full access
    - Manager: Read access
    - Employee: Read access to their company only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            # Managers can read all companies
            if request.user.role == 'manager':
                return True
            # Employees can only read their own company
            if hasattr(request.user, 'employee_profile'):
                return obj == request.user.employee_profile.company
        
        return False


class DepartmentPermission(permissions.BasePermission):
    """
    Department permissions:
    - Admin: Full access
    - Manager: Read access to all, write access to their department
    - Employee: Read access to their department only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role in ['admin', 'manager']

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            # Managers can read all departments
            if request.user.role == 'manager':
                return True
            # Employees can only read their own department
            if hasattr(request.user, 'employee_profile'):
                return obj == request.user.employee_profile.department
        
        # Managers can modify their own department
        if request.user.role == 'manager' and hasattr(request.user, 'employee_profile'):
            return obj == request.user.employee_profile.department
        
        return False


class EmployeePermission(permissions.BasePermission):
    """
    Employee permissions:
    - Admin: Full access
    - Manager: Read access to all, write access to their department employees
    - Employee: Read/write access to their own profile only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role in ['admin', 'manager']

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        # Employees can only access their own profile
        if request.user.role == 'employee':
            return obj.user == request.user
        
        # Managers can access employees in their department
        if request.user.role == 'manager' and hasattr(request.user, 'employee_profile'):
            return obj.department == request.user.employee_profile.department
        
        return False


class ProjectPermission(permissions.BasePermission):
    """
    Project permissions:
    - Admin: Full access
    - Manager: Read access to all, write access to their department projects
    - Employee: Read access to assigned projects, write access to their own projects
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role in ['admin', 'manager']

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        # Employees can read assigned projects and modify their own
        if request.user.role == 'employee' and hasattr(request.user, 'employee_profile'):
            if request.method in permissions.SAFE_METHODS:
                return obj in request.user.employee_profile.assigned_projects.all()
            # Can only modify if they created it (assuming created_by field exists)
            return hasattr(obj, 'created_by') and obj.created_by == request.user.employee_profile
        
        # Managers can access projects in their department
        if request.user.role == 'manager' and hasattr(request.user, 'employee_profile'):
            return obj.department == request.user.employee_profile.department
        
        return False


class PerformanceReviewPermission(permissions.BasePermission):
    """
    Performance Review permissions:
    - Admin: Full access
    - Manager: Read access to all, write access to their department reviews
    - Employee: Read access to their own reviews only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role in ['admin', 'manager']

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'admin':
            return True
        
        # Employees can only access their own reviews
        if request.user.role == 'employee':
            return obj.employee.user == request.user
        
        # Managers can access reviews in their department
        if request.user.role == 'manager' and hasattr(request.user, 'employee_profile'):
            return obj.employee.department == request.user.employee_profile.department
        
        return False
