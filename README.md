# Presence detection node

## Functionality
This is a virtual node. It does not require a specific hardware (except a smart plug for monitoring), and can be executed in the brain of the smart home or any other PC that is connected to the same network as the MQTT broker and that has a bluetooth controller.

Each person that shall be detected must carry a BLE tracker.
When the node is called, the following actions are executed:
* Scan bluetooth devices (several times).
* Search the known MAC addresses of the BLE trackers in the result of the scan.
* For each found device, publish a MQTT information with its RSSI.

## Implementation
Based on the ble-scanner.py script (see external libraries used), I created a layer on top to make it usable for my use case:
* A list linking the target persons to the MAC addresses of their BLE trackers
* Function to extract the useful information: RSSI
* Add MQTT client functionality to publish the detection information.

This module has two resources that may give issues when shared with another concurrent process:
* MQTT client: due to the unique name of the client. Two processes running this node will create two MQTT clients with same name that will try to disconnect each other to establish connection.
* Bluetooth module: I am not sure whether this module implements thread-safe mechanisms, so I'd rather not risk it.

This node is called at different places of Node-Red (e.g: cyclic task, at entrance event...), so it is quite possible that two processes try to use it in parallel. Therefore also implemented a C++ wrapper to ensure that the execution of the node is process safe (see the Audio Node for more details).

## Known issues
* The access to the bluetooth module of the Raspberry Pi must be done with sudo credentials (I haven't found a way to avoid this). This node will be called from an automated task in Node-Red, so I had to give root permission to the Raspberry Pi user where Node-Red is executed, so the sudo password is not requested whenever a program is called with sudo.
* A single scan does not always find all the BLE trackers, therefore it is needed to trigger several scans within the same execution of the node.
* The execution of this node may vary depending on the load of the host. Be careful when calling it with cyclical tasks, ensuring that the maximum execution time is always shorter than the execution cycle.

## Future improvements

## Used hardware
* Smart Plug: https://www.amazon.de/dp/B07D77LFMJ/ref=twister_B07ND6GNDC?_encoding=UTF8&psc=1

## External libraries used
* Python Tuya: https://github.com/clach04/python-tuya
* Paho MQTT client: https://pypi.org/project/paho-mqtt/
