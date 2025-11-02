# WorkTrack API Endpoints

**Base URL:** `http://127.0.0.1:8000/api/`

**Note:** All endpoints require admin authentication (login as superuser first).

---

## 🔐 Authentication

Before testing APIs, you need to log in:
- Go to: `http://127.0.0.1:8000/admin/`
- Login with your superuser credentials
- Or use session-based authentication in your API client

---

## 👤 Employee Endpoints

### 1. List All Employees
```
GET /api/employees/
```
**Query Parameters:**
- `role` - Filter by role (e.g., `?role=Developer`)
- `search` - Search by name or phone number (e.g., `?search=John`)

**Examples:**
- `GET /api/employees/`
- `GET /api/employees/?role=Developer`
- `GET /api/employees/?search=John`

---

### 2. Get Employee Details (with nested projects)
```
GET /api/employees/<id>/
```
**Example:**
- `GET /api/employees/1/`

---

### 3. Create Employee
```
POST /api/employees/
```
**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "role": "Developer",
  "hourly_rate": "50.00"
}
```

---

### 4. Update Employee
```
PUT /api/employees/<id>/
PATCH /api/employees/<id>/
```
**Example:**
- `PUT /api/employees/1/`
- `PATCH /api/employees/1/`

**Request Body (PUT - full update):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "role": "Senior Developer",
  "hourly_rate": "60.00"
}
```

**Request Body (PATCH - partial update):**
```json
{
  "hourly_rate": "65.00"
}
```

---

### 5. Delete Employee
```
DELETE /api/employees/<id>/
```
**Example:**
- `DELETE /api/employees/1/`

---

## 📁 Project Endpoints

### 1. List All Projects
```
GET /api/projects/
```
**Query Parameters:**
- `month` - Filter by month (1-12) (e.g., `?month=11`)
- `year` - Filter by year (e.g., `?year=2025`)
- `search` - Search by name or description (e.g., `?search=website`)

**Examples:**
- `GET /api/projects/`
- `GET /api/projects/?month=11&year=2025`
- `GET /api/projects/?month=11`
- `GET /api/projects/?year=2025`
- `GET /api/projects/?search=website`

---

### 2. Get Project Details (with nested employees and hours)
```
GET /api/projects/<id>/
```
**Example:**
- `GET /api/projects/1/`

---

### 3. Create Project
```
POST /api/projects/
```
**Request Body:**
```json
{
  "name": "Website Redesign",
  "description": "Redesign company website",
  "date": "2025-11-15"
}
```

---

### 4. Update Project
```
PUT /api/projects/<id>/
PATCH /api/projects/<id>/
```
**Example:**
- `PUT /api/projects/1/`
- `PATCH /api/projects/1/`

**Request Body (PUT - full update):**
```json
{
  "name": "Website Redesign v2",
  "description": "Updated description",
  "date": "2025-11-20"
}
```

---

### 5. Delete Project
```
DELETE /api/projects/<id>/
```
**Example:**
- `DELETE /api/projects/1/`

---

## 👤📁 Employee Project Endpoints (Hours Tracking)

### 1. List All Employee-Project Assignments
```
GET /api/employeeprojects/
```
**Query Parameters:**
- `employee` - Filter by employee ID (e.g., `?employee=1`)
- `project` - Filter by project ID (e.g., `?project=1`)
- `date_from` - Filter from date (e.g., `?date_from=2025-11-01`)
- `date_to` - Filter to date (e.g., `?date_to=2025-11-30`)

**Examples:**
- `GET /api/employeeprojects/`
- `GET /api/employeeprojects/?employee=1`
- `GET /api/employeeprojects/?project=1`
- `GET /api/employeeprojects/?employee=1&project=2`
- `GET /api/employeeprojects/?date_from=2025-11-01&date_to=2025-11-30`

---

### 2. Get Employee-Project Assignment Details
```
GET /api/employeeprojects/<id>/
```
**Example:**
- `GET /api/employeeprojects/1/`

---

### 3. Add/Update Employee Hours to Project
```
POST /api/employeeprojects/
```
**Note:** If the employee-project combination already exists, it will update the hours. Otherwise, it creates a new record.

**Request Body:**
```json
{
  "employee": 1,
  "project": 1,
  "hours_worked": 8.5
}
```

---

### 4. Update Employee-Project Hours
```
PUT /api/employeeprojects/<id>/
PATCH /api/employeeprojects/<id>/
```
**Example:**
- `PUT /api/employeeprojects/1/`
- `PATCH /api/employeeprojects/1/`

**Request Body:**
```json
{
  "employee": 1,
  "project": 1,
  "hours_worked": 10.0
}
```

---

### 5. Delete Employee-Project Assignment
```
DELETE /api/employeeprojects/<id>/
```
**Example:**
- `DELETE /api/employeeprojects/1/`

---

## 📊 Statistics Endpoint

### Get Statistics
```
GET /api/statistics/statistics/
```
**Query Parameters:**
- `month` - Filter by month (1-12) (optional)
- `year` - Filter by year (optional)

**Examples:**
- `GET /api/statistics/statistics/` - Overall statistics
- `GET /api/statistics/statistics/?month=11&year=2025` - November 2025 statistics
- `GET /api/statistics/statistics/?year=2025` - All 2025 statistics

**Response:**
```json
{
  "total_employees": 10,
  "total_projects": 25,
  "total_hours": 450.5,
  "month": 11,
  "year": 2025
}
```

---

## 📄 PDF Export Endpoint

### Export Employee Report as PDF
```
GET /api/export-employee/<employee_id>/<month>/?year=<year>
```
**Path Parameters:**
- `employee_id` - Employee ID
- `month` - Month number (1-12)

**Query Parameters:**
- `year` - Year (optional, defaults to current year)

**Examples:**
- `GET /api/export-employee/1/11/?year=2025` - Export employee 1's report for November 2025
- `GET /api/export-employee/2/12/` - Export employee 2's report for December (current year)

**Response:** PDF file download

---

## 🔍 Testing with cURL Examples

### 1. Create Employee
```bash
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "role": "Developer",
    "hourly_rate": "50.00"
  }'
```

### 2. Create Project
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{
    "name": "Website Redesign",
    "description": "Redesign company website",
    "date": "2025-11-15"
  }'
```

### 3. Add Employee Hours to Project
```bash
curl -X POST http://127.0.0.1:8000/api/employeeprojects/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{
    "employee": 1,
    "project": 1,
    "hours_worked": 8.5
  }'
```

### 4. Get All Employees
```bash
curl -X GET http://127.0.0.1:8000/api/employees/ \
  -u admin:password
```

### 5. Get Projects Filtered by Month
```bash
curl -X GET "http://127.0.0.1:8000/api/projects/?month=11&year=2025" \
  -u admin:password
```

### 6. Get Statistics
```bash
curl -X GET "http://127.0.0.1:8000/api/statistics/statistics/?month=11&year=2025" \
  -u admin:password
```

### 7. Export PDF
```bash
curl -X GET "http://127.0.0.1:8000/api/export-employee/1/11/?year=2025" \
  -u admin:password \
  --output employee_report.pdf
```

---

## 📝 Testing with Python Requests

```python
import requests
from requests.auth import HTTPBasicAuth

base_url = "http://127.0.0.1:8000/api"
auth = HTTPBasicAuth('admin', 'password')

# Create employee
response = requests.post(
    f"{base_url}/employees/",
    json={
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "role": "Developer",
        "hourly_rate": "50.00"
    },
    auth=auth
)

# Get all employees
response = requests.get(f"{base_url}/employees/", auth=auth)
print(response.json())

# Create project
response = requests.post(
    f"{base_url}/projects/",
    json={
        "name": "Website Redesign",
        "description": "Redesign company website",
        "date": "2025-11-15"
    },
    auth=auth
)

# Add hours
response = requests.post(
    f"{base_url}/employeeprojects/",
    json={
        "employee": 1,
        "project": 1,
        "hours_worked": 8.5
    },
    auth=auth
)
```

---

## 🌐 Testing in Browser

After logging in at `http://127.0.0.1:8000/admin/`, you can visit:
- `http://127.0.0.1:8000/api/employees/`
- `http://127.0.0.1:8000/api/projects/`
- `http://127.0.0.1:8000/api/employeeprojects/`
- `http://127.0.0.1:8000/api/statistics/statistics/`

---

## 📋 Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees/` | List employees |
| GET | `/api/employees/<id>/` | Get employee details |
| POST | `/api/employees/` | Create employee |
| PUT/PATCH | `/api/employees/<id>/` | Update employee |
| DELETE | `/api/employees/<id>/` | Delete employee |
| GET | `/api/projects/` | List projects |
| GET | `/api/projects/<id>/` | Get project details |
| POST | `/api/projects/` | Create project |
| PUT/PATCH | `/api/projects/<id>/` | Update project |
| DELETE | `/api/projects/<id>/` | Delete project |
| GET | `/api/employeeprojects/` | List assignments |
| GET | `/api/employeeprojects/<id>/` | Get assignment details |
| POST | `/api/employeeprojects/` | Add/update hours |
| PUT/PATCH | `/api/employeeprojects/<id>/` | Update assignment |
| DELETE | `/api/employeeprojects/<id>/` | Delete assignment |
| GET | `/api/statistics/statistics/` | Get statistics |
| GET | `/api/export-employee/<id>/<month>/` | Export PDF |

---

**Note:** Replace `<id>`, `<month>`, and `<year>` with actual values when testing.

