from django.contrib import admin
from .models import Employee, Project, EmployeeProject


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number', 'role', 'hourly_rate', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering = ['last_name', 'first_name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-date', '-created_at']


@admin.register(EmployeeProject)
class EmployeeProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'project', 'hours_worked', 'created_at', 'updated_at']
    list_filter = ['created_at', 'project__date']
    search_fields = ['employee__first_name', 'employee__last_name', 'project__name']
    ordering = ['-created_at']