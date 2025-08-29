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
