# Job Tracking System - Design Document

## 1. Overview
This document outlines the design for the Job Tracking System, which collects and processes job execution counts from SPA and UPCTM environments.

## 2. Expected System Behavior
- The system must fetch job execution counts separately from SPA and UPCTM.
- The system should ensure that both counts are available before aggregation.
- The system should handle missing job counts by either:
  - Raising an explicit error if job count data is unavailable.
  - Logging the issue while allowing partial processing.
- The system must enforce a job execution limit based on BMC licensing constraints.
- If the total job count exceeds **48,500**, an error should be logged, and processing should stop.

## 3. Data Collection
- Job execution counts must be retrieved separately from SPA and UPCTM.
- The system should verify that job counts are successfully fetched from both environments before aggregation.
- If one count is missing, an error should be raised or logged based on configuration.

## 4. Aggregation Logic
- Once job counts are retrieved, they should be summed to compute the total daily job execution count.
- If the total job count exceeds **48,500**, processing should be stopped, and an alert should be generated.
- The system should store the final job count in a persistent database.

## 5. Testing Strategy
- Verify that missing job counts trigger the correct error handling mechanism.
- Test that job count processing prevents exceeding the **48,500** BMC license limit.
- Ensure job counts are realistically capped to fit within constraints.
- Test that job counts can be independently fetched from SPA and UPCTM.
- Validate that both sources contribute to the final total.

## 6. Database Design
- The system should use a lightweight SQL database to store job execution counts.
- The database schema should allow future expansion to include per-application job counts and failure tracking.

## 7. Deployment and Scaling
- The system should be deployable on both **Windows (development)** and **Linux (production)**.
- The database should reside **outside the installation folder** to persist across deployments.

## 8. Future Enhancements
- Support for multiple runs per day with trend analysis.
- Integration with Grafana for real-time monitoring.
- Tracking of job failures and ordered-but-not-running jobs to optimize licensing costs.

---
This document will continue evolving as we refine the design through Test-Driven Development (TDD).

