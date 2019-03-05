import requests
import json
import random
import sys
import getopt
import autodeployconfig as config

# Configuration values
meraki_key = config.merakiapikey
meraki_org = config.merakiorg
meraki_shard = config.merakishard
meraki_url = config.merakiurl
meraki_base_name = config.merakinetbasename
network_devices = config.net_device_config

# Get all devices in the network, remove them, delete the network, recreate
# the network and add devices back in.
def set_network():
    try:
        # Recreate the network
        print("Create the network")
        networkname = meraki_base_name
        url = "https://" + meraki_shard + meraki_url + "organizations/" \
        + meraki_org + "/networks"

        headers = {'X-Cisco-Meraki-API-Key': meraki_key,
                    'Content-Type':'application/json'}

        payload =   {
                        "name": networkname,
                        "type": "wireless switch appliance",
                        "timeZone": "Australia/Melbourne"
                    }

        print(url)
        print(payload)
        response = requests.request("POST", url, data=json.dumps(payload), \
        headers=headers)
        print(response.text)

        # Get the new network ID so we can add the devices
        network = json.loads(response.text)
        network = network["id"]

        return (network)
    except Exception as e:
        print(e)
        sys.exit(1)

def set_devices(network_id):
    try:
        # add devices from config
        print("add the devices")
        for device in network_devices:
            print("add devices from config")
            url = "https://" + meraki_shard + meraki_url + \
            "networks/" +network_id+"/devices/claim"

            payload = {"serial": device}
            headers = {'X-Cisco-Meraki-API-Key': meraki_key,
            'Content-Type': "application/json"}

            response = requests.request("POST", url, \
            data=json.dumps(payload), headers=headers)
            print(response.text)



    except Exception as e:
        print(e)
        sys.exit(1)


def set_ssid(network_id):
    try:
        url = "https://api.meraki.com/api/v0/networks/" + network_id + "/ssids/0"

        payload = "    {\n        \"number\": 0,\n        \"name\": \"CLANZ WiFi\",\n        \"enabled\": true,\n        \"splashPage\": \"None\",\n        \"ssidAdminAccessible\": false,\n        \"encryptionMode\" : \"wpa\",\n        \"wpaEncryptionMode\" : \"WPA2 only\",\n        \"authMode\": \"psk\",\n        \"psk\" : \"clanzwifi\",\n        \"ipAssignmentMode\": \"Bridge mode\",\n        \"minBitrate\": 11,\n        \"bandSelection\": \"5 GHz band only\",\n        \"perClientBandwidthLimitUp\": 0,\n        \"perClientBandwidthLimitDown\": 0\n    }"

        headers = {
            'X-Cisco-Meraki-API-Key': meraki_key,
            'Content-Type': "application/json",
            }

        response = requests.request("PUT", url, data=payload, headers=headers)

        print(response.text)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    network_id = set_network()
    set_devices(network_id)
    set_ssid(network_id)
