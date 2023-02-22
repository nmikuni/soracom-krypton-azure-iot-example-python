import asyncio
import os
import uuid

from azure.iot.device import X509
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

from soracom_krypton_azure_provisioning import SoracomKryptonAzureIoTProvisioning


async def main():
    # This part provisions Azure IoT device using SORACOM Krypton
    target_path = os.getcwd()
    provisioner = SoracomKryptonAzureIoTProvisioning(target_path)
    provision_result = provisioner.provision()
    azure_iot_hub_hostname = provision_result.get('azure_iot_hub_hostname')
    azure_iot_hub_device_id = provision_result.get('azure_iot_hub_device_id')
    cert_file_path = provision_result.get('azure_device_certificate_path')
    key_file_path = provision_result.get('azure_device_private_key_path')

    x509 = X509(cert_file=cert_file_path, key_file=key_file_path)
    device_client = IoTHubDeviceClient.create_from_x509_certificate(
        x509=x509,
        hostname=azure_iot_hub_hostname,
        device_id=azure_iot_hub_device_id,
    )

    # You can write your own code with azure-iot-sdk-python here
    await device_client.connect()
    msg = Message("hello via Krypton!")
    msg.message_id = uuid.uuid4()
    await device_client.send_message(msg)
    await device_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
