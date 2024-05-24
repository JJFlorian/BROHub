import logging

import requests
from django.conf import settings

from api import models as api_models
from api.bro_import import config
from gar.models import GAR
from gmn.models import GMN
from gmw.models import GMW

logger = logging.getLogger(__name__)


class FetchBROIDsError(Exception):
    """Custom exception for errors during BRO IDs fetching."""


class DataImportError(Exception):
    """Custom exception for errors during BRO data import."""


class BulkImporter:
    """Imports bulk data from the BRO for a given KVK and BRO domain.

    It first flushes the current data.
    Then it fetches all BRO id's for the given BRO domain and KVK number.
    Then loops over all id's to import the data if its object.
    Finally, it saves the data in the corresponding datamodel in the database.
    """

    def __init__(self, import_task_instance_uuid: str) -> None:
        # Lookup and update the import task instance
        self.import_task_instance = api_models.ImportTask.objects.get(
            uuid=import_task_instance_uuid
        )
        self.import_task_instance.status = "PROCESSING"
        self.import_task_instance.save()

        self.bro_domain = self.import_task_instance.bro_domain
        self.kvk_number = self.import_task_instance.kvk_number
        self.data_owner = self.import_task_instance.data_owner

        # Lookup the right importer class to initiate for object
        try:
            self.object_importer_class = config.object_importer_mapping[self.bro_domain]
        except Exception as e:
            self.import_task_instance.status = "FAILED"
            self.import_task_instance.log = (
                "The import for this BRO domain is not available yet."
            )
            self.import_task_instance.save()
            raise DataImportError(
                "The import for this BRO domain is not available yet."
            ) from e

    def run(self) -> None:
        try:
            self._flush_existing_data()

            url = self._create_bro_ids_import_url()
            bro_ids = self._fetch_bro_ids(url)

            total_bro_ids = len(bro_ids)
            counter = 0

            for bro_id in bro_ids:
                counter += 1
                progress = (counter / total_bro_ids) * 100
                self.import_task_instance.progress = round(progress, 2)
                self.import_task_instance.save()

                try:
                    data_importer = self.object_importer_class(
                        self.bro_domain, bro_id, self.data_owner
                    )
                    data_importer.run()
                except Exception as e:
                    logger.exception(e)
                    raise DataImportError(
                        f"Error while importing data for bro id: {bro_id}: {e}"
                    ) from e

            self.import_task_instance.status = "COMPLETED"
            self.import_task_instance.save()

        except Exception as e:
            self.import_task_instance.log = e
            self.import_task_instance.status = "FAILED"
            self.import_task_instance.save()

    def _flush_existing_data(self) -> None:
        """Flushes the current data to avoid removed data in the BRO to remain in this db."""
        if self.bro_domain == "GMN":
            GMN.objects.filter(data_owner=self.data_owner).delete()
        if self.bro_domain == "GMW":
            GMW.objects.filter(data_owner=self.data_owner).delete()
        if self.bro_domain == "GAR":
            GAR.objects.filter(data_owner=self.data_owner).delete()

    def _create_bro_ids_import_url(self) -> str:
        """Creates the import url for a given bro object type and kvk combination."""
        bro_domain = self.bro_domain.lower()
        url = f"{settings.BRO_UITGIFTE_SERVICE_URL}/gm/{bro_domain}/v1/bro-ids?bronhouder={self.kvk_number}"
        return url

    def _fetch_bro_ids(self, url: str) -> list:
        """Fetch BRO IDs from the provided URL.

        Returns:
            list: The fetched BRO IDs.
        """
        try:
            r = requests.get(url)
            r.raise_for_status()
            bro_ids = r.json()["broIds"]

            return bro_ids

        except requests.RequestException as e:
            raise FetchBROIDsError(f"Error fetching BRO IDs from {url}: {e}") from e
