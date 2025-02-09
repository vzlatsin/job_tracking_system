from services.job_data_fetcher import JobDataFetcher
from services.job_count_logger import JobCountLogger

class FileJobFetcher(JobDataFetcher):
    """Stub implementation of JobDataFetcher for future file-based job count retrieval."""

    def __init__(self, file_path, logger: JobCountLogger):
        self.file_path = file_path
        self.logger = logger  # ✅ Injecting Logger
        self.class_name = self.__class__.__name__  # ✅ Dynamically store the class name

    def fetch_job_count(self, env):
        """Stub function: Log an attempt to fetch job count and return a placeholder value."""
        self.logger.log_info(f"[{self.class_name}] Fetching job count for {env} from {self.file_path} (FileJobFetcher)")

        # ✅ Instead of returning None, return fixed values
        stub_data = {
            "SPA": 20000,
            "UPCTM": 25000
        }

        return stub_data.get(env, None)  # If env is unknown, return None
