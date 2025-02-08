import unittest
from unittest.mock import MagicMock
import inspect

# Import the classes under test
try:
    from services.job_count_service import JobCountService
    from services.job_count_validator import JobCountValidator
    from services.job_repository import JobRepository
except ImportError as e:
    JobCountService = None
    JobCountValidator = None
    JobRepository = None
    missing_dependency = str(e)

class TestJobCountService(unittest.TestCase):

    def setUp(self):
        """Ensure all necessary objects are defined and validate constructor signature"""
        if JobCountService is None or JobCountValidator is None or JobRepository is None:
            missing = [name for name, obj in [
                ("JobCountService", JobCountService),
                ("JobCountValidator", JobCountValidator),
                ("JobRepository", JobRepository)
            ] if obj is None]
            raise ImportError(f"Missing dependencies: {', '.join(missing)}")

        # Ensure the constructor of JobCountService has expected parameters
        expected_params = {"data_fetcher", "job_repository", "validator"}
        actual_params = set(inspect.signature(JobCountService.__init__).parameters.keys()) - {"self"}

        if expected_params != actual_params:
            raise TypeError(f"Constructor signature mismatch in JobCountService. "
                            f"Expected: {expected_params}, Found: {actual_params}")

        # ✅ Define mock dependencies
        self.mock_fetcher = MagicMock()
        self.mock_validator = MagicMock()
        self.mock_repository = MagicMock()

        # ✅ Inject dependencies into the service
        self.service = JobCountService(
            data_fetcher=self.mock_fetcher,
            job_repository=self.mock_repository,
            validator=self.mock_validator
        )

    def test_fetch_and_process_job_counts(self):
        """Test normal job count retrieval and processing"""
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 20000 if env == "SPA" else 25000

        total_jobs = self.service.process_job_count("SPA", "UPCTM")

        self.assertEqual(total_jobs, 45000)
        self.assertTrue(total_jobs <= 48500, "Job count exceeds BMC license limit!")

    def test_missing_job_count_raises_error(self):
        """Test missing job count raises an error"""
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 20000 if env == "SPA" else None

        with self.assertRaises(ValueError):
            self.service.process_job_count("SPA", "UPCTM")

    def test_exceeding_bmc_license_limit(self):
        """Test exceeding the BMC license limit stops processing"""
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 30000 if env == "SPA" else 20000

        with self.assertRaises(RuntimeError):
            self.service.process_job_count("SPA", "UPCTM")

        self.mock_fetcher.fetch_job_count.assert_called()

    def test_job_count_validation_before_storage(self):
        """Ensure job count is validated before being saved"""
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 20000 if env == "SPA" else 25000

        self.service.process_job_count("SPA", "UPCTM")

        self.mock_validator.validate_counts.assert_called_once_with(20000, 25000)
        self.mock_repository.save_job_count.assert_called_once_with(45000)

if __name__ == '__main__':
    unittest.main()
