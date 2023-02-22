import os
import requests
import time
from urllib.parse import urljoin

RETRY_LIMIT = 10
REQUESTS_TIMEOUT_SEC = 5


class SoracomKryptonAzureIoTProvisioning(object):
    """
    This class provides a way to provision an Azure IoT Hub device using SORACOM Krypton.

    Usage:
    1. Set up Azure IoT Hub and Soracom Group configuration.
    2. Instantiate an instance of this class with a path you want to save the device cert and the device private key.
    3. Call the `provision` method.
    4. If successful, the `provision` method saves the device cert and the device private key as files.
    5. In addition, the `provision` method returns a dictionary containing the Azure IoT Hub hostname, device ID,
    and the path to the device cert and the device private key.

    Example:

    ```
    from soracom_krypton_azure_provisioning import SoracomKryptonAzureIoTProvisioning

    provisioner = SoracomKryptonIoTProvisioning(
        target_path=os.getcwd()
    )
    result = provisioner.provision()
    print(result)
    ```

    Args:
        target_path (str): The path you want to save the device cert and the device private key.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
    """

    def __init__(self, target_path):
        """
        Initialize a new instance of SoracomKryptonAzureIoTProvisioning class.

        Args:
            target_path (str): The path you want to save the device cert and the device private key.

        Raises:
            ValueError: If any of the required parameters are missing or invalid.
        """
        if not os.path.exists(target_path):
            raise ValueError('The path does not exist.')

        self.azure_device_certificate_path = os.path.join(
            target_path, 'certificate.pem')
        self.azure_device_private_key_path = os.path.join(
            target_path, 'privatekey.pem')

    def _save_credential_to_file(self, file_name, file_content):
        with open(file_name, 'w') as f:
            f.write(file_content)

    def provision(self):
        """
        Provision the Azure IoT Hub device with SORACOM Krypton API,
        and save the credentials as files.

        Returns:
            A dictionary containing containing the Azure IoT Hub hostname, device ID,
            and the path to the device cert and the device private key.

        Raises:
            RuntimeError: If provisioning fails
        """
        retry_count = 0
        endpoint = "https://krypton.soracom.io:8036"
        register_path = 'v1/provisioning/azure/iot/register'
        register_url = urljoin(endpoint, register_path)

        try:
            register_response = requests.post(
                register_url, timeout=REQUESTS_TIMEOUT_SEC)
            id = register_response.json().get("operationId")
        except Exception as error:
            raise RuntimeError(
                "Failed to invoke registerAzureIotDevice API. Error: %s" % error)

        if not id:
            raise RuntimeError('Credential issue failed.')

        get_result_path = "v1/provisioning/azure/iot/registrations/%s" % id
        get_result_url = urljoin(endpoint, get_result_path)

        while retry_count < RETRY_LIMIT:
            try:
                get_status_response = requests.get(
                    get_result_url, timeout=REQUESTS_TIMEOUT_SEC)
                device_provisioning_info = get_status_response.json()
            except Exception as error:
                raise RuntimeError(
                    "Failed to invoke getAzureIotDeviceRegistrationStatus API. Error: %s" % error)

            if device_provisioning_info.get('status') == 'assigned':
                break

            retry_count += 1
            time.sleep(1)

        if retry_count == RETRY_LIMIT:
            raise RuntimeError(
                'Credential retreival failed after {} retries'.format(RETRY_LIMIT))

        azure_device_cert = device_provisioning_info.get('certificate')
        self._save_credential_to_file(
            self.azure_device_certificate_path, azure_device_cert)
        azure_device_key = device_provisioning_info.get('privateKey')
        self._save_credential_to_file(
            self.azure_device_private_key_path, azure_device_key)

        return {
            "azure_iot_hub_hostname": device_provisioning_info.get('host'),
            "azure_iot_hub_device_id": device_provisioning_info.get('deviceId'),
            "azure_device_certificate_path": self.azure_device_certificate_path,
            "azure_device_private_key_path": self.azure_device_private_key_path
        }
