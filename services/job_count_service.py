class JobCountService:
    """ Stub version of JobCountService """

    def fetch_job_count(self, env):
        """ Simulate fetching job count for a given environment """
        return 1000 if env == "SPA" else 42000  # Simulated values

    def process_job_count(self, spa_count, upctm_count):
        """ Simulate processing total job count """
        return spa_count + upctm_count  # Simply adds them up
