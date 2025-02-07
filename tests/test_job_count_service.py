import unittest
import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from services.job_count_service import JobCountService 

class TestJobCountService(unittest.TestCase):
    def test_fetch_and_process_job_counts(self):
        service = JobCountService()

        spa_job_count = service.fetch_job_count("SPA")
        upctm_job_count = service.fetch_job_count("UPCTM")

        total_jobs = service.process_job_count(spa_count=spa_job_count, upctm_count=upctm_job_count)

        self.assertEqual(total_jobs, spa_job_count + upctm_job_count)

        bmc_license_limit = 48500
        self.assertTrue(total_jobs <= bmc_license_limit, "Job count exceeds BMC license limit!")

if __name__ == '__main__':
    unittest.main()
