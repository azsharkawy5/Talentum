from django.db import models
from django.db.models import Count
from django.core.validators import MinValueValidator


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def number_of_departments(self):
        return self.departments.count()

    @property
    def number_of_employees(self):
        return self.employees.count()

    @property
    def number_of_projects(self):
        return self.projects.count()


class Department(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["company", "name"]
        ordering = ["company", "name"]

    def __str__(self):
        return f"{self.company.name} - {self.name}"

    @property
    def number_of_employees(self):
        return self.employees.count()

    @property
    def number_of_projects(self):
        return self.projects.count()


class Employee(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees"
    )
    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="employee_profile"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    designation = models.CharField(max_length=255)
    hired_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["company", "department", "name"]

    def __str__(self):
        return f"{self.name} - {self.designation}"

    @property
    def days_employed(self):
        if self.hired_on:
            from datetime import date

            return (date.today() - self.hired_on).days
        return None


class Project(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="projects"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_employees = models.ManyToManyField(
        Employee, related_name="assigned_projects", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["company", "department", "start_date"]

    def __str__(self):
        return f"{self.name} - {self.company.name}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")


class PerformanceReview(models.Model):
    STAGE_CHOICES = [
        ("pending_review", "Pending Review"),
        ("review_scheduled", "Review Scheduled"),
        ("feedback_provided", "Feedback Provided"),
        ("under_approval", "Under Approval"),
        ("review_approved", "Review Approved"),
        ("review_rejected", "Review Rejected"),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="performance_reviews"
    )
    reviewer = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="reviews_conducted",
        null=True,
        blank=True,
    )
    stage = models.CharField(
        max_length=20, choices=STAGE_CHOICES, default="pending_review"
    )
    review_date = models.DateField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        help_text="Rating from 1-5",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Performance Review - {self.employee.name} ({self.get_stage_display()})"

    def can_transition_to(self, new_stage):
        """Check if transition to new stage is allowed"""
        transitions = {
            "pending_review": ["review_scheduled"],
            "review_scheduled": ["feedback_provided"],
            "feedback_provided": ["under_approval"],
            "under_approval": ["review_approved", "review_rejected"],
            "review_rejected": ["feedback_provided"],
            "review_approved": [],
        }
        return new_stage in transitions.get(self.stage, [])
