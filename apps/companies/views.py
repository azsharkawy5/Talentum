from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Company, Department, Employee, Project, PerformanceReview
from .serializers import (
    CompanySerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    ProjectSerializer,
    PerformanceReviewSerializer,
)
from .permissions import (
    CompanyPermission,
    DepartmentPermission,
    EmployeePermission,
    ProjectPermission,
    PerformanceReviewPermission,
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


# Project Views
class ProjectListView(generics.ListCreateAPIView):
    """
    List all projects and create new ones (admin/manager only)
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["company", "department", "start_date", "end_date"]
    search_fields = ["name", "description"]
    ordering_fields = [
        "name",
        "start_date",
        "end_date",
        "company__name",
        "department__name",
    ]
    ordering = ["company__name", "department__name", "start_date"]

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


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a project
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]


# Performance Review Views
class PerformanceReviewListView(generics.ListCreateAPIView):
    """
    List all performance reviews and create new ones (admin/manager only)
    """

    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [PerformanceReviewPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["employee", "stage", "reviewer"]
    search_fields = ["employee__name", "feedback", "notes"]
    ordering_fields = ["created_at", "review_date", "stage"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Filter by user's company if employee
        if user.role == "employee" and hasattr(user, "employee_profile"):
            queryset = queryset.filter(employee__company=user.employee_profile.company)
        # Filter by user's department if manager
        elif user.role == "manager" and hasattr(user, "employee_profile"):
            queryset = queryset.filter(
                employee__department=user.employee_profile.department
            )

        return queryset


class PerformanceReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a performance review
    """

    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [PerformanceReviewPermission]


class PerformanceReviewTransitionView(generics.GenericAPIView):
    """
    Handle stage transitions for performance reviews
    """

    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [PerformanceReviewPermission]

    def post(self, request, pk=None):
        review = self.get_object()
        new_stage = request.data.get("new_stage")

        if not new_stage:
            return Response(
                {"error": "new_stage is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not review.can_transition_to(new_stage):
            return Response(
                {
                    "error": f"Cannot transition from {review.get_stage_display()} to {dict(PerformanceReview.STAGE_CHOICES)[new_stage]}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        review.stage = new_stage
        review.save()

        serializer = self.get_serializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
