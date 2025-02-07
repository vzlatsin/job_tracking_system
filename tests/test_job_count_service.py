import unittest
import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from services.job_count_service import JobCountService 

class TestJobCountService(unittest.TestCase):
    def setUp(self):
        """ Initialize service before each test """
        self.service = JobCountService()  # ✅ This ensures self.service is available in all tests
        
    def test_fetch_and_process_job_counts(self):
        """ Test fetching job counts and processing total count """
        spa_job_count = self.service.fetch_job_count("SPA")
        upctm_job_count = self.service.fetch_job_count("UPCTM")

        total_jobs = self.service.process_job_count(spa_count=spa_job_count, upctm_count=upctm_job_count)

        self.assertEqual(total_jobs, spa_job_count + upctm_job_count)

        bmc_license_limit = 48500
        self.assertTrue(total_jobs <= bmc_license_limit, "Job count exceeds BMC license limit!")


    def test_missing_job_count(self):
        """ Test scenario where SPA job count is missing (simulated as None) """
        spa_job_count = None  # Simulate missing job count
        upctm_job_count = self.service.fetch_job_count("UPCTM")

        with self.assertRaises(ValueError):  # Expect an error
            self.service.process_job_count(spa_count=spa_job_count, upctm_count=upctm_job_count)


if __name__ == '__main__':
    unittest.main()
