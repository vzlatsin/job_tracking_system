from services.job_data_fetcher import JobDataFetcher  # ✅ Import the base class

class JobCountService:
    def __init__(self, data_fetcher: JobDataFetcher):
        """Inject a JobDataFetcher subclass (Database, API, File)."""
        self.data_fetcher = data_fetcher

    def process_job_count(self, env1, env2):
        """Fetch job counts from the injected fetcher and sum them."""
        count1 = self.data_fetcher.fetch_job_count(env1)
        count2 = self.data_fetcher.fetch_job_count(env2)

        if count1 is None or count2 is None:
            # print(f"DEBUG: Missing job count detected (count1={count1}, count2={count2})")  # Debugging
            raise ValueError("Job count missing!")
        
        # print(f"DEBUG: count1={count1}, count2={count2}, total={count1 + count2}")  # Debugging

        if count1 + count2 > 48500:
            raise RuntimeError("Job count exceeds BMC license limit!")


        return count1 + count2
