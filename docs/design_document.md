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

## **Appendix B: How TDD Shaped Our System Design**

### **B.1 Overview**
Test-Driven Development (TDD) has been instrumental in shaping the architecture of the Job Tracking System. By writing tests before implementing functionality, we ensured that:
- Each component has a **clear and testable responsibility**.
- The design evolved **incrementally**, avoiding overengineering.
- Dependencies were **mocked and injected**, reducing coupling and improving modularity.

### **B.2 Catching Errors Early During the Design Phase**
During the design phase, the system's **metadata (class dependencies, method signatures, and parameters) is highly volatile**. TDD helps by:
- **Failing early when an object is missing**, ensuring dependencies are properly structured before implementation.
- **Providing immediate feedback when constructor signatures change**, preventing breaking changes from propagating unnoticed.
- **Allowing for incremental improvements**, guiding design choices naturally without overengineering.

### **B.3 How Tests Drove the Design**
Initially, we wrote tests for fundamental system requirements:
- **Fetching job counts correctly** (`test_fetch_and_process_job_counts`)
- **Handling missing job counts properly** (`test_missing_job_count_raises_error`)
- **Ensuring job count limits are enforced** (`test_exceeding_bmc_license_limit`)
- **Ensuring dependency injection is correctly structured**

These tests **forced us to introduce `JobCountService`** as a separate abstraction to handle business logic while keeping data fetching independent. **Without TDD, we might have prematurely coupled these concerns.**

### **B.4 How TDD Prevented Bad Design**
1. **Encapsulation of Business Logic**
   - Our first test failed when a job count was missing.
   - Instead of handling this inside the database layer, TDD guided us to **centralize validation inside `JobCountService`**.

2. **Separation of Concerns**
   - Early test failures revealed that we needed clear separation between **data fetching, processing, and storage**.
   - This resulted in **better modularity**, making the system easier to maintain.

3. **Immediate Detection of Architectural Inconsistencies**
   - When new dependencies were introduced, **tests broke immediately**, alerting us to missing parameters in constructor signatures.
   - This helped ensure that **each change was intentional and well-integrated** into the design.

### **B.5 Evolution of System Architecture Through TDD**
Each test failure guided refinements in system design:
| **Test Case** | **Impact on System Design** |
|--------------|--------------------------|
| Missing job count raises `ValueError` | Led to explicit validation in `JobCountService` |
| Exceeding BMC license limit stops processing | Led to early failure conditions for excessive counts |
| Dependency injection failures | Forced validation of constructor parameters in tests |
| Ensuring metadata stability | Led to the introduction of early validation checks for missing classes |

### **B.6 Next Steps in TDD**
As we expand the system, TDD will drive:
- **Database persistence validation** (ensuring only valid counts are stored).
- **Retries and error handling** (ensuring the system remains robust under failures).
- **Refactoring opportunities** (keeping the design clean and modular).

By continuing this approach, we ensure that **our system evolves in a testable, maintainable, and elegant way while catching errors as early as possible in the design phase.**

