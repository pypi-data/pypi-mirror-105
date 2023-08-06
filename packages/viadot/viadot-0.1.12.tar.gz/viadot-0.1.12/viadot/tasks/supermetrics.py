import prefect
from prefect import Task
from typing import Dict, Any
from ..sources import Supermetrics


class SupermetricsToCSV(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(name="supermetrics_to_csv", *args, **kwargs)

    def __call__(self):
        """Download Supermetrics data to a CSV"""

    def run(self, query: Dict[str, Any], path: str):

        logger = prefect.context.get("logger")

        # Build the URL
        supermetrics = Supermetrics()
        supermetrics.query(query)

        # Download data to a local CSV file
        logger.info(f"Downloading data to {path}...")
        supermetrics.to_csv(path)
        logger.info(f"Successfully downloaded data to {path}.")
