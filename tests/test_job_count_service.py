import unittest
from unittest.mock import MagicMock
from services.job_count_service import JobCountService  # Assuming this exists

class TestJobCountService(unittest.TestCase):

    def setUp(self):
        """Set up JobCountService with a fake job count fetcher"""
        self.mock_fetcher = MagicMock()  # Create a fake job count fetcher
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 20000 if env == "SPA" else 25000
        self.service = JobCountService(data_fetcher=self.mock_fetcher)  # Inject the fake fetch method

    def test_fetch_and_process_job_counts(self):
        """Test normal job count retrieval and processing"""
        # Define fake return values for job counts
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 20000 if env == "SPA" else 25000

        total_jobs = self.service.process_job_count("SPA", "UPCTM")

        self.assertEqual(total_jobs, 45000)  # 20000 + 25000
        self.assertTrue(total_jobs <= 48500, "Job count exceeds BMC license limit!")

    def test_missing_job_count_raises_error(self):
        """Test missing job count raises an error"""
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 20000 if env == "SPA" else None

        with self.assertRaises(ValueError):  # Expect failure
            self.service.process_job_count("SPA", "UPCTM")

    def test_exceeding_bmc_license_limit(self):
        """Test exceeding the BMC license limit stops processing"""
        self.mock_fetcher.fetch_job_count.side_effect = lambda env: 30000 if env == "SPA" else 20000

        # Check if the mock returns the correct values
        # print(f"TEST DEBUG: SPA returns {self.mock_fetcher.fetch_job_count('SPA')}")
        # print(f"TEST DEBUG: UPCTM returns {self.mock_fetcher.fetch_job_count('UPCTM')}")

        with self.assertRaises(RuntimeError):
            self.service.process_job_count("SPA", "UPCTM")
            
        self.mock_fetcher.fetch_job_count.assert_called()  # ✅ Ensure the mock was actually used


if __name__ == '__main__':
    unittest.main()
