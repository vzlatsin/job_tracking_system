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

## 5. System Architecture (Object Design)
The system follows **object-oriented design best practices**, ensuring modularity, extensibility, and testability.

### **5.1 Key Design Principles**
- **Single Responsibility Principle (SRP)**: Each class has **only one reason to change**.
- **Dependency Injection**: Objects **receive dependencies instead of creating them**.
- **Separation of Concerns**: Processing logic is separate from database interactions.
- **Composition Over Inheritance**: Objects **collaborate via composition rather than deep inheritance**.
- **Open-Closed Principle**: The system **can be extended without modifying existing classes**.

### **5.2 Class Overview**
| **Class Name**        | **Responsibility** |
|----------------------|-------------------|
| `JobDataFetcher`      | Abstract class that defines the method `fetch_job_count(env)`. |
| `DatabaseJobFetcher`  | Retrieves job counts from a database (subclass of `JobDataFetcher`). |
| `JobCountService`     | Handles the **aggregation logic** and applies business rules (e.g., missing counts, max limits). |
| `JobRepository`       | Saves valid job counts to the database. |
| `JobTrackingApp`      | Orchestrates the overall workflow, calling services and repositories. |

### **5.3 Class Interactions**
1. `JobTrackingApp` **calls** `JobCountService`.
2. `JobCountService` **fetches data** from `JobDataFetcher`.
3. `JobDataFetcher` **retrieves job counts** (via database, API, or files).
4. `JobCountService` **validates job counts** (checking missing data and max limits).
5. If validation **passes**, `JobCountService` **stores data** using `JobRepository`.

---

## 6. Testing Strategy
- **Mocking:** The system was tested using a **mocked `JobDataFetcher`** to verify:
  - **Fetching job counts correctly** from SPA and UPCTM.
  - **Handling missing job counts by raising `ValueError`**.
  - **Stopping processing if the job count exceeds 48,500** (`RuntimeError`).
- **Validation of Database Logic:**
  - Ensure only **valid, complete job counts** are stored in the database.

## 7. Database Design
- The system uses a **lightweight SQL database** to store daily job execution counts.
- The database schema ensures **only valid job counts** are saved (no partial data).
- Future expansion includes **per-application job tracking** and **job failure tracking**.

## 8. Deployment and Scaling
- The system is **developed on Windows** and **deployed on Linux**.
- The database resides **outside the installation folder** for persistence across deployments.

## 9. Future Enhancements
- Support for **multiple runs per day** to track trends.
- Integration with **Grafana for real-time monitoring**.
- Tracking of **failed jobs** and **ordered-but-not-running jobs** to optimize BMC licensing costs.

---

## **Appendix: System Architecture Best Practices**
Below are the **key principles** that must be followed when designing system architecture.

### **A.1 Single Responsibility Principle (SRP)**
✅ **What is it?**  
Each class **should have only one responsibility** and **one reason to change**.  
✅ **Why is it important?**  
- If a class **does too many things**, modifying one feature **can break another**.  
- **Smaller, focused classes** are easier to **debug, extend, and test**.  

### **A.2 Dependency Injection (DI)**
✅ **What is it?**  
Instead of a class **creating objects inside itself**, we **pass objects to it**.  
✅ **Why is it important?**  
- **Increases flexibility** (you can swap dependencies easily).  
- **Enables testing** (you can mock dependencies).  

### **A.3 Separation of Concerns (SoC)**
✅ **What is it?**  
Different parts of the system **should not mix responsibilities** (business logic, data storage, UI, etc.).  
✅ **Why is it important?**  
- **Keeps code maintainable** (changing one layer does not affect others).  
- **Prevents bugs** from spreading across unrelated parts of the system.  

### **A.4 Composition Over Inheritance**
✅ **What is it?**  
Prefer **using objects together (composition)** instead of **making everything a subclass (inheritance).**  
✅ **Why is it important?**  
- **Avoids deep inheritance chains** (which become hard to debug).  
- **Allows flexible object combinations** without changing base classes.  

### **A.5 Open-Closed Principle (OCP)**
✅ **What is it?**  
A system should be **open for extension but closed for modification**.  
✅ **Why is it important?**  
- **New features can be added without modifying existing code** (less risk of breaking existing functionality).  

### **A.6 Testability**
✅ **What is it?**  
The system should be **easily testable using unit tests and mocks**.  
✅ **Why is it important?**  
- **Prevents regressions** (bugs when changing code).  
- **Ensures business rules work correctly**.  

### **A.7 Scalability and Maintainability**
✅ **What is it?**  
The system should be **designed to grow over time** and be easy to maintain.  
✅ **Why is it important?**  
- **Prevents bottlenecks** when adding new features.  
- **Ensures long-term usability**.  

## **Appendix B: How TDD Shaped Our System Design**

### **B.1 Overview**
Test-Driven Development (TDD) has been instrumental in shaping the architecture of the Job Tracking System. By writing tests before implementing functionality, we ensured that:
- Each component has a **clear and testable responsibility**.
- The design evolved **incrementally**, avoiding overengineering.
- Dependencies were **mocked and injected**, reducing coupling and improving modularity.

### **B.2 How Tests Drove the Design**
Initially, we wrote tests for fundamental system requirements:
- **Fetching job counts correctly** (`test_fetch_and_process_job_counts`)
- **Handling missing job counts properly** (`test_missing_job_count_raises_error`)
- **Ensuring job count limits are enforced** (`test_exceeding_bmc_license_limit`)

These tests **forced us to introduce `JobCountService`** as a separate abstraction to handle business logic while keeping data fetching independent. **Without TDD, we might have prematurely coupled these concerns.**

### **B.3 How TDD Prevented Bad Design**
1. **Encapsulation of Business Logic**
   - Our first test failed when a job count was missing.
   - Instead of handling this inside the database layer, TDD guided us to **centralize validation inside `JobCountService`**.

2. **Separation of Concerns**
   - Early test failures revealed that we needed clear separation between **data fetching, processing, and storage**.
   - This resulted in **better modularity**, making the system easier to maintain.

3. **Improved Dependency Injection**
   - Writing tests required us to **mock `JobDataFetcher`** to isolate `JobCountService` logic.
   - This led to a **better architecture where `JobCountService` receives dependencies instead of creating them**.

### **B.4 Evolution of System Architecture Through TDD**
Each test failure guided refinements in system design:
| **Test Case** | **Impact on System Design** |
|--------------|--------------------------|
| Missing job count raises `ValueError` | Led to explicit validation in `JobCountService` |
| Exceeding BMC license limit stops processing | Led to early failure conditions for excessive counts |
| Database persistence test | Led to the creation of `JobRepository` for storing only valid data |

### **B.5 Next Steps in TDD**
As we expand the system, TDD will drive:
- **Database persistence validation** (ensuring only valid counts are stored).
- **Retries and error handling** (ensuring the system remains robust under failures).
- **Refactoring opportunities** (keeping the design clean and modular).

By continuing this approach, we ensure that **our system evolves in a testable, maintainable, and elegant way.**



---
This document evolves as we refine the design through **Test-Driven Development (TDD)**.

