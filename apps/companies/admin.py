from django.contrib import admin
from .models import Company, Department, Employee, Project, PerformanceReview


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_departments', 'number_of_employees', 'number_of_projects', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['number_of_departments', 'number_of_employees', 'number_of_projects', 'created_at', 'updated_at']
    ordering = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'number_of_employees', 'number_of_projects', 'created_at']
    list_filter = ['company', 'created_at']
    search_fields = ['name', 'company__name']
    readonly_fields = ['number_of_employees', 'number_of_projects', 'created_at', 'updated_at']
    ordering = ['company__name', 'name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'department', 'designation', 'hired_on', 'days_employed', 'created_at']
    list_filter = ['company', 'department', 'designation', 'hired_on', 'created_at']
    search_fields = ['name', 'email', 'designation']
    readonly_fields = ['days_employed', 'created_at', 'updated_at']
    ordering = ['company__name', 'department__name', 'name']
    raw_id_fields = ['user']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'department', 'start_date', 'end_date', 'assigned_employees_count', 'created_at']
    list_filter = ['company', 'department', 'start_date', 'end_date', 'created_at']
    search_fields = ['name', 'description', 'company__name', 'department__name']
    readonly_fields = ['assigned_employees_count', 'created_at', 'updated_at']
    ordering = ['company__name', 'department__name', 'start_date']
    filter_horizontal = ['assigned_employees']
    
    def assigned_employees_count(self, obj):
        return obj.assigned_employees.count()
    assigned_employees_count.short_description = 'Assigned Employees'


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'stage', 'review_date', 'rating', 'created_at']
    list_filter = ['stage', 'rating', 'review_date', 'created_at']
    search_fields = ['employee__name', 'reviewer__name', 'feedback', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    raw_id_fields = ['employee', 'reviewer']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee', 'reviewer', 'stage')
        }),
        ('Review Details', {
            'fields': ('review_date', 'rating', 'feedback', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
