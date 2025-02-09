from services.job_count_logger import JobCountLogger

class JobRepository:
    """Stub for Job Repository"""

    def __init__(self, logger: JobCountLogger):
        self.logger = logger  # ✅ Injected logger
        self.class_name = self.__class__.__name__  # ✅ Dynamically store the class name

    def save_job_count(self, count):
        self.logger.log_info(f"[{self.class_name}] Saving job count: {count}")
        pass  # Stub implementation

