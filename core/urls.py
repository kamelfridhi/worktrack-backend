from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'employeeprojects', views.EmployeeProjectViewSet, basename='employeeproject')
router.register(r'statistics', views.StatisticsViewSet, basename='statistics')

urlpatterns = [
    # Include all router URLs
    path('', include(router.urls)),
    # PDF export endpoint: /api/export-employee/<id>/<month>/?year=2025
    path('export-employee/<int:employee_id>/<int:month>/', views.export_employee_pdf, name='export-employee-pdf'),
]
