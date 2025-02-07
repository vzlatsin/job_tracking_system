class JobCountService:
    """ Handles job count processing (Stub Version) """

    def fetch_job_count(self, env):
        """ Simulate fetching job count for a given environment """
        return 1000 if env == "SPA" else 42000  # Simulated values

    def process_job_count(self, spa_count, upctm_count):
        """ Validate and compute total job count """
        
        # ✅ Handle missing values (None)
        if spa_count is None or upctm_count is None:
            raise ValueError("[ERROR] Missing job count from one of the environments!")

        total_jobs = spa_count + upctm_count

        # ✅ Enforce BMC License Limit
        bmc_license_limit = 48000
        if total_jobs > bmc_license_limit:
            raise ValueError(f"[ERROR] Job count {total_jobs} exceeds BMC license limit ({bmc_license_limit})!")

        return total_jobs
