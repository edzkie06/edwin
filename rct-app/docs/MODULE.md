# MODULES

## Overview

This document describes all modules available in the KPI Agent Management System, including their purpose and main functions.

---

# 1. Authentication

## Purpose
Handles user authentication and session management.

### Features
- User Login
- User Logout
- Remember Session
- Password Validation
- Account Lock (Future)

### Permissions
- All Users

---

# 2. Dashboard

## Purpose
Displays an overview of system performance and KPI statistics.

### Features
- KPI Summary
- Agent Summary
- Site Summary
- Charts
- Quick Statistics

### Permissions
- ADMIN
- OM
- AOM
- TL
- STAFF (View Only)

---

# 3. Agent Management

## Purpose
Manage all agent information.

### Features
- Add Agent
- Edit Agent
- View Agent
- Search Agent
- Filter Agent

### Permissions

| Role | Access |
|------|--------|
| ADMIN | Full |
| OM | Full |
| AOM | Full |
| TL | Edit Assigned Team |
| STAFF | View Only |

---

# 4. KPI Management

## Purpose
Manage KPI records and monitor performance.

### Features
- Add KPI
- Edit KPI
- View KPI
- KPI History
- KPI Computation

### Permissions

| Role | Access |
|------|--------|
| ADMIN | Full |
| OM | Full |
| AOM | Full |
| TL | Assigned Team |
| STAFF | View Only |

---

# 5. MPS Management

## Purpose
Manage Monthly Performance Score (MPS).

### Features
- Input MPS
- Edit MPS
- View MPS
- Import MPS
- Search MPS

### Permissions

| Role | View | Input | Edit | Import |
|------|------|-------|------|--------|
| ADMIN | ✓ | ✓ | ✓ | ✓ |
| OM | ✓ | ✓ | ✓ | ✓ |
| AOM | ✓ | ✓ | ✓ | ✓ |
| TL | ✓ | ✓ | ✓ | ✓ |
| STAFF | ✓ | ✗ | ✗ | ✗ |

---

# 6. Site Management

## Purpose
Manage all supported sites.

### Features
- View Sites
- Add Site
- Edit Site
- Site Dashboard

---

# 7. User Management

## Purpose
Manage system users.

### Features
- Create User
- Edit User
- Reset Password
- Activate User
- Deactivate User

### Permissions

| Role | Access |
|------|--------|
| ADMIN | Full |
| OM | Full |
| AOM | Limited |
| TL | None |
| STAFF | None |

---

# 8. Role & Permission

## Purpose
Control user access throughout the system.

### Roles
- ADMIN
- OM
- AOM
- TL
- STAFF

---

# 9. Audit Logs

## Purpose
Record important activities performed within the system.

### Records
- Login
- Logout
- Create
- Update
- Delete
- Import
- Export
- IP Address
- Browser
- Operating System
- Timestamp

### Permissions

| Role | View | Edit |
|------|------|------|
| ADMIN | ✓ | ✓ |
| OM | ✓ | ✓ |
| AOM | ✓ | ✓ |
| TL | ✓ | ✗ |
| STAFF | ✗ | ✗ |

---

# 10. Reports

## Purpose
Generate printable and exportable reports.

### Features
- KPI Report
- MPS Report
- Agent Report
- Export PDF
- Export Excel

---

# 11. Settings

## Purpose
Manage system configuration.

### Features
- Theme
- System Settings
- Site Configuration
- Maintenance Settings

---

# Future Modules

- Notifications
- Email Alerts
- API Integration
- Activity Dashboard
- Backup & Restore