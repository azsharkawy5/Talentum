from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Company, Department, Employee
from .serializers import (
    CompanySerializer,
    DepartmentSerializer,
    EmployeeSerializer,
)
from .permissions import (
    CompanyPermission,
    DepartmentPermission,
    EmployeePermission,
)


# Company Views
class CompanyListView(generics.ListAPIView):
    """
    List all companies (read-only for non-admin users)
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [CompanyPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class CompanyDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single company (read-only for non-admin users)
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [CompanyPermission]


# Department Views
class DepartmentListView(generics.ListCreateAPIView):
    """
    List all departments and create new ones (admin/manager only)
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["company", "name"]
    search_fields = ["name"]
    ordering_fields = ["name", "company__name", "created_at"]
    ordering = ["company__name", "name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Filter by user's company if employee
        if user.role == "employee" and hasattr(user, "employee_profile"):
            queryset = queryset.filter(company=user.employee_profile.company)

        return queryset


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a department
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermission]


# Employee Views
class EmployeeListView(generics.ListCreateAPIView):
    """
    List all employees and create new ones (admin/manager only)
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeePermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["company", "department", "designation"]
    search_fields = ["name", "email", "designation"]
    ordering_fields = [
        "name",
        "company__name",
        "department__name",
        "hired_on",
        "created_at",
    ]
    ordering = ["company__name", "department__name", "name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Filter by user's company if employee
        if user.role == "employee" and hasattr(user, "employee_profile"):
            queryset = queryset.filter(company=user.employee_profile.company)
        # Filter by user's department if manager
        elif user.role == "manager" and hasattr(user, "employee_profile"):
            queryset = queryset.filter(department=user.employee_profile.department)

        return queryset


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete an employee
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeePermission]


class EmployeeProfileView(generics.RetrieveUpdateAPIView):
    """
    Employee can view and update their own profile
    """

    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.employee_profile
