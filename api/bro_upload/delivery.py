import time
import traceback

from . import config
from lxml.etree import _Element

from . import utils


class XMLValidationError(Exception):
    """Exception raised when XML validation fails."""

    pass


class DeliveryError(Exception):
    """Exception raised when the delivery has an error."""

    pass


class BRODelivery:
    """Handles the complete process of uploading data to the BRO.

    During the initialization, a XML-generator class is defined based on the provided registration_type.
    This class instance is then used to create the XML file for the Delivery.
    The rest of the delivery process is handled by this class.

    The steps of the complete process are:
        1) Generation of the XML File.
        2) Validation of the XML File with the BRO webservice.
        3) Delivery of the XML file to the BRO.
        4) The check of the delivery status.
        5) Finalization of the whole process.
    """

    def __init__(
        self,
        upload_task_instance: str,
        bro_username: str,
        bro_password: str,
        project_number: str,
    ) -> None:
        self.upload_task_instance = upload_task_instance
        self.bro_username = bro_username
        self.bro_password = bro_password
        self.project_number = project_number
        self.bro_domain = self.upload_task_instance.bro_domain
        self.registration_type = self.upload_task_instance.registration_type
        self.request_type = self.upload_task_instance.registration_type
        self.metadata = self.upload_task_instance.metadata
        self.sourcedocument_data = self.upload_task_instance.sourcedocument_data
        self.xml_generator_class = config.xml_generator_mapping.get(
            self.registration_type
        )

    def process(self) -> None:
        # Generate the XML file.
        xml_file = self._generate_xml_file()
        print(xml_file)

        # Validate with the BRO API
        self._validate_xml_file(xml_file)

        # Deliver the XML file. The deliver_url is returned to use for the check.
        deliver_url = self._deliver_xml_file(xml_file)

        # Check of the status of the delivery. Retries 3 times before failing
        retries_count = 0

        while retries_count < 4:
            if self._check_delivery(deliver_url):
                return
            else:
                time.sleep(10)
                retries_count += 1
    
        raise DeliveryError(f"Delivery was unsuccesfull")

    def _generate_xml_file(self) -> _Element:
        try:
            generator = self.xml_generator_class(
                self.request_type, self.metadata, self.sourcedocument_data
            )
            return generator.create_xml_file()

        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"Error generating XML file: {e}") from e

    def _validate_xml_file(self, xml_file: _Element) -> None:
        validation_response = utils.validate_xml_file(
            xml_file, self.bro_username, self.bro_password, self.project_number
        )

        if validation_response["status"] != "VALIDE":
            raise XMLValidationError(
                f"Errors while validating the XML file: {validation_response['errors']}"
            )
        else:
            return

    def _deliver_xml_file(self, xml_file: _Element) -> str:
        """The upload consists of 4 steps:
        1) Requesting an upload by posting to the BRO api. Returns an upload_url
        2) Adding the XML file to the upload
        3) The actual delivery
        """

        upload_id = utils.create_upload_id(
            self.bro_username, self.bro_password, self.project_number
        )
        utils.add_xml_to_upload(
            xml_file,
            upload_id,
            self.bro_username,
            self.bro_password,
            self.project_number,
        )
        delivery_url = utils.create_delivery(
            upload_id, self.bro_username, self.bro_password, self.project_number
        )

        return delivery_url

    def _check_delivery(self, delivery_url: str) -> bool:
        """Checks the delivery status."""

        delivery_info = utils.check_delivery_status(
            delivery_url, self.bro_username, self.bro_password
        )

        errors = delivery_info.json()["brondocuments"][0]["errors"]
        if errors:
            raise DeliveryError(f"Errors found after delivering the XML file: {errors}")

        else:
            delivery_status = delivery_info.json()["status"]
            delivery_brondocument_status = delivery_info["brondocuments"][0]["status"]

            if (
                delivery_status == "DOORGELEVERD"
                and delivery_brondocument_status == "OPGENOMEN_LVBRO"
            ):
                return True

            else:
                return False
