from rest_framework import serializers
from .models import Employee, Project, EmployeeProject


class EmployeeProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for EmployeeProject with project details.
    """
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_date = serializers.DateField(source='project.date', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)

    class Meta:
        model = EmployeeProject
        fields = ['id', 'project_id', 'project_name', 'project_date', 'hours_worked', 'created_at']


class ProjectEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for EmployeeProject with employee details.
    """
    employee_name = serializers.CharField(source='employee.__str__', read_only=True)
    employee_id = serializers.IntegerField(source='employee.id', read_only=True)
    employee_phone_number = serializers.CharField(source='employee.phone_number', read_only=True)

    class Meta:
        model = EmployeeProject
        fields = ['id', 'employee_id', 'employee_name', 'employee_phone_number', 'hours_worked', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee with nested projects.
    """
    employee_projects = EmployeeProjectSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'phone_number',
            'role', 'hourly_rate', 'created_at', 'employee_projects'
        ]
        read_only_fields = ['created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EmployeeListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Employee list view (without nested data).
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'full_name', 'phone_number', 'role', 'hourly_rate']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project with nested employees and their hours.
    """
    employee_projects = ProjectEmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'date', 'created_at', 'employee_projects'
        ]
        read_only_fields = ['created_at']


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Project list view (without nested data).
    """
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'date', 'created_at', 'employee_count']

    def get_employee_count(self, obj):
        """Return the count of employees assigned to this project."""
        return obj.employee_projects.count()


class EmployeeProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating EmployeeProject.
    Handles upsert logic (update if exists, create if not).
    """
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    hours_worked = serializers.FloatField(required=False, default=0.0, allow_null=False)

    class Meta:
        model = EmployeeProject
        fields = ['id', 'employee', 'project', 'hours_worked', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        """
        Create or update EmployeeProject record.
        If record exists for same employee and project, update hours_worked.
        """
        employee = validated_data['employee']
        project = validated_data['project']
        hours_worked = validated_data.get('hours_worked', 0.0)

        employee_project, created = EmployeeProject.objects.update_or_create(
            employee=employee,
            project=project,
            defaults={'hours_worked': hours_worked}
        )

        return employee_project
