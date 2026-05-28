This project focuses on cleaning, validating, and structuring "noisy" employee and payroll data from various CSV files, followed by importing the verified data into a robust SQLite database.

## 📊 Project File Structure

The project utilizes and generates the following datasets and files:

*   **Raw (Noisy) Data:**
    *   `employees_noisy.csv` — Contains raw employee data with inconsistent formatting, missing values, or date anomalies.
    *   `payroll_noisy.csv` — Contains raw payroll records with potential outliers (e.g., negative hours, invalid period formats).
*   **Cleaned & Validated Data:**
    *   `employees_clean.csv` — Standardized and deduplicated employee records.
    *   `payroll_clean.csv` — Cleaned and filtered payroll entries.
    *   `payroll_validated.csv` — Final verified payroll records matching all database constraints, ready for staging.
*   **Database:**
    *   `EmployeeManagement.db` — The target SQLite database where the final structured data is stored.

---

## 🛠️ Data Validation & Business Rules

To ensure data integrity, the pipeline enforces strict validation constraints before inserting data into the database:

### 1. Employees Table
*   `EmployeeID`: Unique Identifier (Primary Key).
*   `FirstName` & `LastName`: Mandatory fields (NOT NULL).
*   `Salary`: Must be a positive value and cannot exceed the corporate ceiling.  
    $$\text{Salary} > 0 \quad \text{AND} \quad \text{Salary} \le 500,000$$
*   `HireDate`: All dates are standardized to the ISO `YYYY-MM-DD` format (handling older variations like `MM/DD/YYYY`).

### 2. Payroll Table
*   `HoursWorked`: Must be a realistic amount of work hours per week.  
    $$0 \le \text{HoursWorked} \le 168$$
*   `Bonus` & `Deductions`: Must be non-negative values ($\ge 0$).
*   `PayPeriod`: Standardized to `YYYY-MM-DD`. Invalid entries or legacy formats (e.g., `Jan-2024` or literal text like `invalid`) are filtered or corrected.

---

## 🗄️ Database Architecture (SQLite)

The `EmployeeManagement.db` database is structured with relational tables, automation triggers, and summary views:

### 1. Core Tables
*   **`Employees`**: Holds core staff information (Department, Hire Date, Salary).
*   **`Payroll`**: Tracks hours worked, bonuses, and deductions per period, linked via a `FOREIGN KEY` to `Employees`.
*   **`SalaryHistory`**: An audit log table that automatically archives compensation adjustments.

### 2. Database Triggers
*   **`LogSalaryChange`**: An `AFTER UPDATE` trigger on the `Employees` table. Whenever an employee's salary is modified, it automatically logs the `EmployeeID`, `OldSalary`, `NewSalary`, and the exact `CURRENT_TIMESTAMP` into the `SalaryHistory` table.

### 3. Database Views
*   **`DepartmentPayrollSummary`**: An analytical view aggregating data by `Department` to provide quick business insights:
    *   **Total Employees** (`TotalEmployees`)
    *   **Total Hours Worked** (`TotalHoursWorked`)
    *   **Total Bonuses Paid** (`TotalBonus`)
    *   **Average Department Salary** (`AverageSalary`)

---

## 🚀 How to Run the Pipeline

1. **Clean the Datasets:** Run the data processing script to clean the noisy CSV inputs.
```bash
   python clean_data.p