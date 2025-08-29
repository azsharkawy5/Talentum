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
