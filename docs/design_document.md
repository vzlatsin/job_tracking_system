# Job Tracking System - Design Document

## 1. Overview
This document outlines the design for the Job Tracking System, which collects and processes job execution counts from SPA and UPCTM environments.

## 2. Expected System Behavior
- The system must fetch job execution counts separately from **SPA** and **UPCTM**.
- Both counts **must be available before aggregation**. Partial processing **is not allowed**.
- If a job count is **missing**, the system must **raise a `ValueError`** instead of proceeding.
- If the total job count exceeds **48,500**, processing must **stop immediately** and raise a `RuntimeError`.

## 3. Data Collection
- Job execution counts are retrieved from **SPA** and **UPCTM** using the `JobDataFetcher` class.
- The system ensures that **both counts are successfully fetched** before aggregation.
- If a count is missing, **an error is raised immediately** to prevent incorrect calculations.

## 4. Aggregation Logic
- Once job counts are retrieved, they are summed to compute the **total daily job execution count**.
- If the total job count exceeds **48,500**, a **`RuntimeError` is raised**, stopping processing.
- The system **stores the valid total job count** in a **persistent SQL database**.
- No partial or incomplete job counts are ever stored.

## 5. Testing Strategy
- **Mocking:** The system was tested using a **mocked `JobDataFetcher`** to verify:
  - **Fetching job counts correctly** from SPA and UPCTM.
  - **Handling missing job counts by raising `ValueError`**.
  - **Stopping processing if the job count exceeds 48,500** (`RuntimeError`).
- **Validation of Database Logic:**
  - Ensure only **valid, complete job counts** are stored in the database.

## 6. Database Design
- The system uses a **lightweight SQL database** to store daily job execution counts.
- The database schema ensures **only valid job counts** are saved (no partial data).
- Future expansion includes **per-application job tracking** and **job failure tracking**.

## 7. Deployment and Scaling
- The system is **developed on Windows** and **deployed on Linux**.
- The database resides **outside the installation folder** for persistence across deployments.

## 8. Future Enhancements
- Support for **multiple runs per day** to track trends.
- Integration with **Grafana for real-time monitoring**.
- Tracking of **failed jobs** and **ordered-but-not-running jobs** to optimize BMC licensing costs.

---
This document evolves as we refine the design through **Test-Driven Development (TDD)**.
