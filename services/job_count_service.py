from services.job_data_fetcher import JobDataFetcher  # ✅ Fetches job counts
from services.job_count_validator import JobCountValidator  # ✅ Handles validation
from services.job_repository import JobRepository  # ✅ Stores job counts
from services.job_count_logger import JobCountLogger  # ✅ Ensure logger is imported

class JobCountService:
    def __init__(self, data_fetcher: JobDataFetcher, job_repository: JobRepository, validator: JobCountValidator, logger: JobCountLogger):
        """Inject dependencies for fetching, validating, and storing job counts."""
        self.data_fetcher = data_fetcher
        self.job_repository = job_repository
        self.validator = validator
        self.logger = logger  # ✅ Assign logger instance

        self.MAX_BMC_LIMIT = 48500  # ✅ Restore BMC license limit

    def process_job_count(self, env1, env2):
        """Fetch, validate, enforce limits, and store job counts."""
        self.logger.log_info(f"Fetching job counts from {env1} and {env2}")  # ✅ Log start

        count1 = self.data_fetcher.fetch_job_count(env1)
        count2 = self.data_fetcher.fetch_job_count(env2)

        if count1 is None or count2 is None:
            self.logger.log_error("Job count missing!")  # ✅ Ensure logging happens
            raise ValueError("Job count missing!")

        # ✅ Validate job counts before proceeding
        self.validator.validate_counts(count1, count2)

        total_count = count1 + count2
        # ✅ Ensure success log is called before storing the job count
        self.logger.log_info(f"Job count validated successfully. Storing count: {total_count}") 

        # ✅ Enforce BMC license limit before storing
        if total_count > self.MAX_BMC_LIMIT:
            self.logger.log_error(f"Job count exceeds BMC license limit! (Total: {total_count})")  # ✅ Ensure logging before raising error
            raise RuntimeError(f"Job count exceeds BMC license limit! (Total: {total_count})")

        # ✅ Store only valid job counts
        self.job_repository.save_job_count(total_count)

        return total_count
