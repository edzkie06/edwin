# API DOCUMENTATION

## Overview

This document contains all application routes (API/Flask Routes) used in the KPI Agent Management System.

---

# Authentication

## Login

| Method | Route | Permission |
|--------|-------|------------|
| POST | /login | Public |

Description:
Authenticate user credentials.

---

## Logout

| Method | Route | Permission |
|--------|-------|------------|
| GET | /logout | Logged-in Users |

Description:
Ends the current user session.

---

# Dashboard

## Dashboard

| Method | Route | Permission |
|--------|-------|------------|
| GET | /dashboard | All Roles |

Description:
Display dashboard summary.

---

# Agent Management

## Agent List

| Method | Route | Permission |
|--------|-------|------------|
| GET | /agents | ADMIN, OM, AOM, TL |

Description:
Display all agents.

---

## Add Agent

| Method | Route | Permission |
|--------|-------|------------|
| POST | /agents/add | ADMIN, OM, AOM |

Description:
Create a new agent.

---

## Edit Agent

| Method | Route | Permission |
|--------|-------|------------|
| POST | /agents/edit/<id> | ADMIN, OM, AOM, TL |

Description:
Update agent information.

---

## Delete Agent

| Method | Route | Permission |
|--------|-------|------------|
| POST | /agents/delete/<id> | ADMIN, OM |

Description:
Delete an agent.

---

# MPS

## View MPS

| Method | Route | Permission |
|--------|-------|------------|
| GET | /mps | ADMIN, OM, AOM, TL, STAFF |

Description:
Display MPS records.

---

## Input MPS

| Method | Route | Permission |
|--------|-------|------------|
| POST | /mps/add | ADMIN, OM, AOM, TL |

Description:
Add MPS record.

---

## Edit MPS

| Method | Route | Permission |
|--------|-------|------------|
| POST | /mps/edit/<id> | ADMIN, OM, AOM, TL |

Description:
Update MPS record.

---

## Import MPS

| Method | Route | Permission |
|--------|-------|------------|
| POST | /mps/import | ADMIN, OM, AOM, TL |

Description:
Import MPS from Excel.

---

# User Management

## User List

| Method | Route | Permission |
|--------|-------|------------|
| GET | /users | ADMIN, OM |

Description:
Display all users.

---

## Create User

| Method | Route | Permission |
|--------|-------|------------|
| POST | /users/add | ADMIN, OM |

Description:
Create a system user.

---

## Edit User

| Method | Route | Permission |
|--------|-------|------------|
| POST | /users/edit/<id> | ADMIN, OM |

Description:
Modify user information.

---

## Reset Password

| Method | Route | Permission |
|--------|-------|------------|
| POST | /users/reset-password/<id> | ADMIN, OM |

Description:
Reset user password.

---

# Audit Logs

## View Logs

| Method | Route | Permission |
|--------|-------|------------|
| GET | /audit-logs | ADMIN, OM, AOM, TL |

Description:
Display audit history.

---

## Export Logs

| Method | Route | Permission |
|--------|-------|------------|
| GET | /audit-logs/export | ADMIN, OM, AOM |

Description:
Export audit logs.

---

# Reports

## Generate Report

| Method | Route | Permission |
|--------|-------|------------|
| GET | /reports | ADMIN, OM, AOM, TL |

Description:
Generate reports.

---

## Export Excel

| Method | Route | Permission |
|--------|-------|------------|
| GET | /reports/export/excel | ADMIN, OM, AOM, TL |

Description:
Export report to Excel.

---

## Export PDF

| Method | Route | Permission |
|--------|-------|------------|
| GET | /reports/export/pdf | ADMIN, OM, AOM, TL |

Description:
Export report to PDF.

---

# Settings

## View Settings

| Method | Route | Permission |
|--------|-------|------------|
| GET | /settings | ADMIN, OM |

Description:
Display system settings.

---

## Update Settings

| Method | Route | Permission |
|--------|-------|------------|
| POST | /settings/update | ADMIN |

Description:
Update system configuration.

---

# Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

# Notes

- All protected routes require user authentication.
- Permissions are enforced based on the user's role.
- All Create, Update, Delete, Import, and Export actions should be recorded in the Audit Logs.
- Future API endpoints should be documented in this file before implementation.