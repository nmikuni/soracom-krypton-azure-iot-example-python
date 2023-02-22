# Example for SORACOM Krypton with Azure IoT Hub

With this example, you can use SORACOM Krypton to provision Azure IoT devices.

For details, please refer to the documents.

- EN: https://developers.soracom.io/en/docs/krypton/azure-iot/
- JA: https://users.soracom.io/ja-jp/docs/krypton/azure-iot-hub/

In this repository, there are 2 Python files.

1. **soracom_krypton_azure_provisioning.py**: It has the class SoracomKryptonAzureIoTProvisioning to provision Azure IoT devices
2. **send_data_to_azure.py**: Provision the device with SoracomKryptonAzureIoTProvisioning and send data to Azure IoT Hub
   
## How to use

1. Set up SORACOM and Azure with the document above. You need to run this program on the device connected to the SORACOM network.
2. Install azure-iot-sdk-python with `python -m pip install azure-iot-device`.
3. Run send_data_to_azure.py
4. You can customize send_data_to_azure.py with your own code using azure-iot-sdk-python.