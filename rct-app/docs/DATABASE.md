# DATABASE

## Overview

This document describes the database structure of the KPI Agent Management System.

Database Engine:
- MySQL

---

# Database Relationship

Users
│
├── Audit Logs
│
├── MPS
│
├── KPI
│
└── Agents

Sites
│
├── Agents
│
├── KPI
│
└── MPS

---

# Table: users

## Purpose

Stores all system user accounts.

### Primary Key

- id

### Columns

| Column | Type | Description |
|---------|------|-------------|
| id | INT | User ID |
| username | VARCHAR | Login username |
| password | VARCHAR | Encrypted password |
| fullname | VARCHAR | Full name |
| role | VARCHAR | User role |
| site | VARCHAR | Assigned site |
| status | VARCHAR | Active / Inactive |
| created_at | DATETIME | Creation date |

---

# Table: agents

## Purpose

Stores all agent information.

### Primary Key

- id

### Columns

| Column | Type | Description |
|---------|------|-------------|
| id | INT | Agent ID |
| employee_id | VARCHAR | Employee Number |
| fullname | VARCHAR | Agent Name |
| site | VARCHAR | Assigned Site |
| team_leader | VARCHAR | Assigned TL |
| status | VARCHAR | Active / Resigned |

---

# Table: kpi

## Purpose

Stores KPI records.

### Columns

| Column | Type | Description |
|---------|------|-------------|
| id | INT | KPI ID |
| agent_id | INT | Agent Reference |
| month | VARCHAR | KPI Month |
| score | DECIMAL | KPI Score |
| remarks | TEXT | Comments |

---

# Table: mps

## Purpose

Stores Monthly Performance Score.

### Columns

| Column | Type | Description |
|---------|------|-------------|
| id | INT | Record ID |
| agent_id | INT | Agent Reference |
| month | VARCHAR | Month |
| score | DECIMAL | MPS Score |
| created_by | INT | User ID |

---

# Table: audit_logs

## Purpose

Stores all important system activities.

### Columns

| Column | Type | Description |
|---------|------|-------------|
| id | INT | Log ID |
| user_id | INT | User Reference |
| action | VARCHAR | Action performed |
| module | VARCHAR | Module name |
| ip_address | VARCHAR | User IP |
| browser | VARCHAR | Browser |
| operating_system | VARCHAR | OS |
| created_at | DATETIME | Timestamp |

---

# Relationships

users
    │
    ├── audit_logs
    ├── mps
    └── kpi

agents
    │
    ├── kpi
    └── mps

sites
    │
    ├── users
    ├── agents
    ├── kpi
    └── mps

---

# Future Tables

- notifications
- reports
- system_settings
- backup_logs