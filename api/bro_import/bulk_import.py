import requests

from django.conf import settings
from .. import models
from . import object_import

class FetchBROIDsError(Exception):
    """Custom exception for errors during BRO IDs fetching."""

class BulkImporter:
    """ Imports data from the BRO for a given KVK and BRO domain.
    
    It first fetches all BRO id's for the given BRO domain and KVK number.
    Then loops over all id's to import the data if its object.
    Finally, it saves the data in the corresponding datamodel in the database.
    """

    def __init__(self, import_task_instance_uuid):
        self.import_task_instance = models.ImportTask.objects.get(
            uuid=import_task_instance_uuid
        )
        self.bro_domain = self.import_task_instance.bro_domain
        self.organisation = self.import_task_instance.organisation
        self.kvk_number = self.organisation.kvk_number

        # Lookup the right importer class to initiate for obje
        object_importer_mapping = {
            "GMN":object_import.GMNObjectImporter,
            "GMW":object_import.GMWObjectImporter,
            "GLD":object_import.GLDObjectImporter,
            "FRD":object_import.FRDObjectImporter,
        }

        self.object_importer = object_importer_mapping[self.bro_domain]

    def run(self):
        bro_ids = self._fetch_bro_ids()
        
        for bro_id in bro_ids:
            self.object_importer(bro_id)

    def _fetch_bro_ids(self) -> list:
        """Fetch BRO IDs from the provided URL.

        Returns:
            list: The fetched BRO IDs.
        """
        url = self._create_bro_ids_import_url()

        try:
            r = requests.get(url)
            r.raise_for_status() 
            bro_ids = r.json()["broIds"]
            
            return bro_ids
        
        except requests.RequestException as e:
            raise FetchBROIDsError(f"Error fetching BRO IDs from {url}: {e}") from e
        
    def _create_bro_ids_import_url(self) -> str:
        """ Creates the import url for a given bro object type and kvk combination.       
        """
        bro_domain = self.bro_domain.lower()
        url = f"{settings.BRO_UITGIFTE_SERVICE_URL}/gm/{bro_domain}/v1/bro-ids?bronhouder={self.kvk_number}"
        return url
    
