from rest_framework import serializers
from .models import Company, Department, Employee, Project, PerformanceReview


class CompanySerializer(serializers.ModelSerializer):
    number_of_departments = serializers.ReadOnlyField()
    number_of_employees = serializers.ReadOnlyField()
    number_of_projects = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "number_of_departments",
            "number_of_employees",
            "number_of_projects",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class DepartmentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    number_of_employees = serializers.ReadOnlyField()
    number_of_projects = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = [
            "id",
            "company",
            "company_name",
            "name",
            "number_of_employees",
            "number_of_projects",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "company_name",
            "number_of_employees",
            "number_of_projects",
            "created_at",
            "updated_at",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    days_employed = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "company",
            "company_name",
            "department",
            "department_name",
            "user",
            "name",
            "email",
            "mobile_number",
            "address",
            "designation",
            "hired_on",
            "days_employed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "company_name",
            "department_name",
            "days_employed",
            "created_at",
            "updated_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    assigned_employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "company",
            "company_name",
            "department",
            "department_name",
            "name",
            "description",
            "start_date",
            "end_date",
            "assigned_employees",
            "assigned_employees_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "company_name",
            "department_name",
            "assigned_employees_count",
            "created_at",
            "updated_at",
        ]

    def get_assigned_employees_count(self, obj):
        return obj.assigned_employees.count()

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("End date must be after start date")

        return attrs


class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)
    reviewer_name = serializers.CharField(source="reviewer.name", read_only=True)
    stage_display = serializers.CharField(source="get_stage_display", read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "employee_name",
            "reviewer",
            "reviewer_name",
            "stage",
            "stage_display",
            "review_date",
            "feedback",
            "rating",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee_name",
            "reviewer_name",
            "stage_display",
            "created_at",
            "updated_at",
        ]

    def validate_stage(self, value):
        """Validate stage transitions"""
        instance = self.instance
        if instance and not instance.can_transition_to(value):
            current_stage = instance.get_stage_display()
            raise serializers.ValidationError(
                f"Cannot transition from '{current_stage}' to '{dict(PerformanceReview.STAGE_CHOICES)[value]}'"
            )
        return value

    def validate_rating(self, value):
        """Validate rating range"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
