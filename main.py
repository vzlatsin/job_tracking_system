from services.data_fetchers.file_fetcher import FileJobFetcher
from services.job_count_service import JobCountService
from services.job_count_validator import JobCountValidator
from services.job_repository import JobRepository
from services.job_count_logger import JobCountLogger

def main():
    """Initialize and run the Job Tracking System."""
    print("🔹 Starting Job Tracking System...")

    # ✅ Initialize components
    logger = JobCountLogger()
    file_fetcher = FileJobFetcher("job_counts.txt", logger)  # ✅ Using stub fetcher
    job_repository = JobRepository(logger)  # This still needs a real implementation
    validator = JobCountValidator()

    # ✅ Initialize the main service
    job_service = JobCountService(
        data_fetcher=file_fetcher,  # ✅ Injecting stub fetcher
        job_repository=job_repository,
        validator=validator,
        logger=logger
    )

    # ✅ Fetch and process job counts
    try:
        job_service.process_job_count("SPA", "UPCTM")
        print("✅ Job count processing completed (Placeholder values used).")
    except Exception as e:
        logger.log_error(f"❌ Error occurred: {str(e)}")
        print(f"❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
