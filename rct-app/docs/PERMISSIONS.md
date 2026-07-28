# PERMISSIONS

## Overview

This document defines the access rights of every role in the KPI Agent Management System.

---

# Roles

| Role | Description |
|------|-------------|
| ADMIN | Full system access |
| OM | Operations Manager |
| AOM | Assistant Operations Manager |
| TL | Team Leader |
| STAFF | Staff / Encoder |

---

# Permission Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Allowed |
| ❌ | Not Allowed |
| 👁 | View Only |

---

# Dashboard

| Role | Access |
|------|--------|
| ADMIN | ✅ |
| OM | ✅ |
| AOM | ✅ |
| TL | ✅ |
| STAFF | ✅ |

---

# Agent Management

| Role | View | Add | Edit | Delete |
|------|------|-----|------|--------|
| ADMIN | ✅ | ✅ | ✅ | ✅ |
| OM | ✅ | ✅ | ✅ | ✅ |
| AOM | ✅ | ✅ | ✅ | ❌ |
| TL | ✅ | ❌ | ✅ | ❌ |
| STAFF | 👁 | ❌ | ❌ | ❌ |

---

# KPI Management

| Role | View | Add | Edit | Delete |
|------|------|-----|------|--------|
| ADMIN | ✅ | ✅ | ✅ | ✅ |
| OM | ✅ | ✅ | ✅ | ✅ |
| AOM | ✅ | ✅ | ✅ | ❌ |
| TL | ✅ | ❌ | ✅ | ❌ |
| STAFF | 👁 | ❌ | ❌ | ❌ |

---

# MPS Management

| Role | View | Input | Edit | Delete | Import |
|------|------|-------|------|--------|--------|
| ADMIN | ✅ | ✅ | ✅ | ✅ | ✅ |
| OM | ✅ | ✅ | ✅ | ✅ | ✅ |
| AOM | ✅ | ✅ | ✅ | ❌ | ✅ |
| TL | ✅ | ✅ | ✅ | ❌ | ✅ |
| STAFF | 👁 | ❌ | ❌ | ❌ | ❌ |

---

# User Management

| Role | View | Create | Edit | Delete | Reset Password |
|------|------|--------|------|--------|----------------|
| ADMIN | ✅ | ✅ | ✅ | ✅ | ✅ |
| OM | ✅ | ✅ | ✅ | ❌ | ✅ |
| AOM | 👁 | ❌ | ❌ | ❌ | ❌ |
| TL | ❌ | ❌ | ❌ | ❌ | ❌ |
| STAFF | ❌ | ❌ | ❌ | ❌ | ❌ |

---

# Audit Logs

| Role | View | Edit |
|------|------|------|
| ADMIN | ✅ | ✅ |
| OM | ✅ | ✅ |
| AOM | ✅ | ✅ |
| TL | 👁 | ❌ |
| STAFF | ❌ | ❌ |

---

# Reports

| Role | View | Export |
|------|------|--------|
| ADMIN | ✅ | ✅ |
| OM | ✅ | ✅ |
| AOM | ✅ | ✅ |
| TL | ✅ | ✅ |
| STAFF | 👁 | ❌ |

---

# Settings

| Role | View | Edit |
|------|------|------|
| ADMIN | ✅ | ✅ |
| OM | ✅ | ✅ |
| AOM | 👁 | ❌ |
| TL | ❌ | ❌ |
| STAFF | ❌ | ❌ |

---

# Future Permissions

- Approval Workflow
- Export Restrictions
- Site-based Permissions
- Module-based Permissions