class JobDataFetcher:
    """Base class for fetching job counts from different sources (DB, API, File)."""

    def fetch_job_count(self, env):
        """Fetch job execution count for the given environment (SPA or UPCTM)."""
        raise NotImplementedError("fetch_job_count() must be implemented in a subclass.")
