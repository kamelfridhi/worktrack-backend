from django.db import models


class Employee(models.Model):
    """
    Employee model representing a worker in the system.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    """
    Project model representing a work project.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(help_text="The workday for this project")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.name} ({self.date})"


class EmployeeProject(models.Model):
    """
    Relation table linking employees to projects with hours worked.
    If an employee works on the same project on the same date, the record is updated.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='employee_projects')
    hours_worked = models.FloatField(help_text="Hours worked on this project")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['employee', 'project']
        verbose_name_plural = 'Employee Projects'

    def __str__(self):
        return f"{self.employee} - {self.project}: {self.hours_worked}h"