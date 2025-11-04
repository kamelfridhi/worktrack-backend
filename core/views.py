import os
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import KeepInFrame
from io import BytesIO
import os
from django.conf import settings

from .models import Employee, Project, EmployeeProject
from .serializers import (
    EmployeeSerializer, EmployeeListSerializer,
    ProjectSerializer, ProjectListSerializer,
    EmployeeProjectCreateSerializer, EmployeeProjectSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Custom login endpoint for frontend authentication.
    GET: Returns CSRF token for initial setup
    POST: Authenticates user and logs them in
    """
    if request.method == 'GET':
        # Return CSRF token for initial setup
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token})

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_staff:
        django_login(request, user)
        # Ensure session is saved
        request.session.save()
        # Ensure CSRF token is set in cookie
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        response = Response({
            'success': True,
            'message': 'Login successful',
            'sessionid': request.session.session_key
        })
        # Explicitly set session cookie headers
        # In production (HTTPS), use SameSite=None and Secure=True for cross-origin
        # Check if we're on cloud (Render, Railway, etc.) - if so, always use HTTPS settings
        from django.conf import settings
        ON_CLOUD = os.environ.get('RENDER') or os.environ.get('RAILWAY') or os.environ.get('DYNO')
        is_https = ON_CLOUD or request.is_secure()

        response.set_cookie(
            'sessionid',
            request.session.session_key,
            max_age=86400,  # 24 hours
            path='/',
            domain=None,  # Let browser handle domain (None means current domain)
            secure=is_https,  # True in production (HTTPS), False for localhost
            httponly=True,
            samesite='None' if is_https else 'Lax'  # None for cross-origin HTTPS, Lax for localhost
        )
        return response
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def api_logout(request):
    """
    Custom logout endpoint.
    """
    from django.contrib.auth import logout as django_logout
    django_logout(request)
    return Response({'success': True, 'message': 'Logout successful'})


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations.
    Returns full details with nested projects in detail view,
    simplified list in list view.
    """
    queryset = Employee.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer

    def get_queryset(self):
        """
        Filter employees by role, phone number, or name if provided.
        """
        queryset = Employee.objects.all()
        role = self.request.query_params.get('role', None)
        search = self.request.query_params.get('search', None)

        if role:
            queryset = queryset.filter(role__icontains=role)

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_number__icontains=search)
            )

        return queryset


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Project CRUD operations.
    Supports filtering by month and year.
    Returns full details with nested employees in detail view.
    """
    queryset = Project.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        """
        Filter projects by month, year, or specific date if provided.
        Example: /api/projects/?month=11&year=2025
        Example: /api/projects/?date=2025-11-02
        """
        queryset = Project.objects.all()
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)
        date = self.request.query_params.get('date', None)
        search = self.request.query_params.get('search', None)

        # If specific date is provided, filter by that exact date
        if date:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except (ValueError, TypeError):
                # If date format is invalid, ignore the date filter
                pass
        else:
            # Otherwise, use month/year filtering
            if month:
                queryset = queryset.filter(date__month=month)

            if year:
                queryset = queryset.filter(date__year=year)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset


class EmployeeProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EmployeeProject CRUD operations.
    Supports filtering by employee, project, and date.
    Automatically updates existing records if employee+project combination exists.
    """
    queryset = EmployeeProject.objects.select_related('employee', 'project').all()
    serializer_class = EmployeeProjectCreateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Filter employee projects by employee, project, or date range.
        """
        queryset = EmployeeProject.objects.select_related('employee', 'project').all()
        employee_id = self.request.query_params.get('employee', None)
        project_id = self.request.query_params.get('project', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        if date_from:
            queryset = queryset.filter(project__date__gte=date_from)

        if date_to:
            queryset = queryset.filter(project__date__lte=date_to)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override list to use a serializer that includes related data.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = EmployeeProjectSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EmployeeProjectSerializer(queryset, many=True)
        return Response(serializer.data)


def export_employee_pdf(request, employee_id, month):
    """
    Generate a PDF report for an employee's work in a specific month/year.
    Endpoint: /api/export-employee/<id>/<month>/
    Query parameter: year (optional, defaults to current year)
    Note: The month parameter should be the month number (1-12).
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return HttpResponse('Employee not found', status=404)

    # Get year from query parameter or use current year
    year = request.GET.get('year', timezone.now().year)
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return HttpResponse('Invalid month or year parameter', status=400)

    # Get all employee projects for the specified month/year
    employee_projects = EmployeeProject.objects.filter(
        employee=employee,
        project__date__year=year,
        project__date__month=month
    ).select_related('project').order_by('project__date')

    # Calculate total hours
    total_hours = sum(ep.hours_worked for ep in employee_projects)

    # Check if employee has hourly rate
    has_hourly_rate = employee.hourly_rate is not None and employee.hourly_rate > 0

    # Calculate total earnings if hourly rate exists
    total_earnings = 0
    if has_hourly_rate:
        total_earnings = total_hours * float(employee.hourly_rate)

    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=10,
        alignment=1,  # Center alignment
    )
    org_style = ParagraphStyle(
        'OrgStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1800ad'),
        spaceAfter=5,
        alignment=1,  # Center alignment
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
    )
    normal_style = styles['Normal']
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=2,  # Right alignment
    )
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
    )

    # Add header with logo and organization name
    # Try to load logo if it exists in static files
    logo_path = None
    try:
        # Check if logo exists in static files
        static_logo_path = os.path.join(settings.BASE_DIR, 'static', 'logo_transp.png')
        if os.path.exists(static_logo_path):
            logo_path = static_logo_path
    except:
        pass

    # Create header table with logo and organization name
    if logo_path:
        try:
            logo = Image(logo_path, width=2*inch, height=0.8*inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 0.1 * inch))
        except:
            pass

    # Organization name
    elements.append(Paragraph("ZeenAlZein", org_style))
    elements.append(Spacer(1, 0.1 * inch))

    # Add title
    title = Paragraph(f"Mitarbeiter Arbeitsbericht", title_style)
    elements.append(title)

    # Add print date/time (in German format)
    month_names_german = {
        1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',
        5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
    }
    now = datetime.now()
    month_name_print = month_names_german.get(now.month, f"Monat {now.month}")
    day = now.day
    year_print = now.year
    hour = now.hour
    minute = now.minute
    # Format time in 24-hour format
    time_str = f"{hour:02d}:{minute:02d} Uhr"
    print_datetime = f"{month_name_print} {day}, {year_print} um {time_str}"
    elements.append(Paragraph(f"<i>Gedruckt: {print_datetime}</i>", date_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Add employee information
    elements.append(Paragraph(f"<b>Mitarbeiter:</b> {employee.first_name} {employee.last_name}", normal_style))
    elements.append(Paragraph(f"<b>Telefonnummer:</b> {employee.phone_number}", normal_style))
    elements.append(Paragraph(f"<b>Rolle:</b> {employee.role}", normal_style))
    if employee.hourly_rate:
        elements.append(Paragraph(f"<b>Stundensatz:</b> €{employee.hourly_rate:.2f}", normal_style))

    # Month/Year info
    month_names = {
        1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',
        5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
    }
    month_name = month_names.get(int(month), f"Monat {month}")
    elements.append(Paragraph(f"<b>Zeitraum:</b> {month_name} {year}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Add projects table
    if employee_projects:
        elements.append(Paragraph(f"<b>Bearbeitete Projekte</b>", heading_style))

        # Prepare table headers - conditionally include earnings column
        if has_hourly_rate:
            table_data = [
                [Paragraph('<b>Datum</b>', normal_style),
                 Paragraph('<b>Projektname</b>', normal_style),
                 Paragraph('<b>Gearbeitete Stunden</b>', normal_style),
                 Paragraph('<b>Betrag</b>', normal_style)]
            ]
        else:
            table_data = [
                [Paragraph('<b>Datum</b>', normal_style),
                 Paragraph('<b>Projektname</b>', normal_style),
                 Paragraph('<b>Gearbeitete Stunden</b>', normal_style)]
            ]

        # Add project rows
        for ep in employee_projects:
            if has_hourly_rate:
                earnings = ep.hours_worked * float(employee.hourly_rate)
                table_data.append([
                    ep.project.date.strftime('%Y-%m-%d'),
                    ep.project.name,
                    f"{ep.hours_worked:.2f}",
                    f"€{earnings:.2f}"
                ])
            else:
                table_data.append([
                    ep.project.date.strftime('%Y-%m-%d'),
                    ep.project.name,
                    f"{ep.hours_worked:.2f}"
                ])

        # Add total row - conditionally include earnings
        if has_hourly_rate:
            total_row = [
                '',
                Paragraph('<b>GESAMTSTUNDEN</b>', bold_style),
                Paragraph(f'<b>{total_hours:.2f}</b>', bold_style),
                Paragraph(f'<b>€{total_earnings:.2f}</b>', bold_style)
            ]
        else:
            total_row = [
                '',
                Paragraph('<b>GESAMTSTUNDEN</b>', bold_style),
                Paragraph(f'<b>{total_hours:.2f}</b>', bold_style)
            ]
        table_data.append(total_row)

        # Define column widths based on whether earnings column exists
        if has_hourly_rate:
            col_widths = [1.5 * inch, 2.8 * inch, 1.2 * inch, 1.5 * inch]
            # Right align hours and amount columns
            align_rules = [
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),  # Hours column
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),  # Amount column
            ]
        else:
            col_widths = [1.5 * inch, 3.5 * inch, 1.5 * inch]
            # Right align hours column
            align_rules = [
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),  # Hours column
            ]

        # Create table
        table = Table(table_data, colWidths=col_widths)
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            *align_rules,  # Add conditional alignment rules
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TOPPADDING', (0, -1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
        ]
        table.setStyle(TableStyle(table_style))

        elements.append(table)
    else:
        elements.append(Paragraph(f"Für {month_name} {year} wurden keine Projekte gefunden", normal_style))

    # Build PDF
    doc.build(elements)

    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()

    # Create response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    filename = f"employee_{employee_id}_report_{year}_{month:02d}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


class StatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet for statistics endpoint.
    Returns total projects, total employees, and total hours for a month.
    """
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get statistics for the system or a specific month/year.
        Query params: month, year (optional)
        """
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)

        # Total employees
        total_employees = Employee.objects.count()

        # Total projects (optionally filtered by month/year)
        projects_query = Project.objects.all()
        if month:
            projects_query = projects_query.filter(date__month=month)
        if year:
            projects_query = projects_query.filter(date__year=year)
        total_projects = projects_query.count()

        # Total hours (optionally filtered by month/year)
        hours_query = EmployeeProject.objects.all()
        if month:
            hours_query = hours_query.filter(project__date__month=month)
        if year:
            hours_query = hours_query.filter(project__date__year=year)

        total_hours_result = hours_query.aggregate(total=Sum('hours_worked'))
        total_hours = total_hours_result['total'] or 0.0

        return Response({
            'total_employees': total_employees,
            'total_projects': total_projects,
            'total_hours': round(total_hours, 2),
            'month': int(month) if month else None,
            'year': int(year) if year else None,
        })
