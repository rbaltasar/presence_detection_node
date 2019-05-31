# test BLE Scanning software

import blescan
import sys
from time import sleep
import paho.mqtt.client as paho

import bluetooth._bluetooth as bluez

#Cris / Raul / Cris car / Tag black / 
#mac_id_list = ["de:c4:53:4c:d5:04","c3:09:89:ed:66:de","ea:d5:67:64:e1:67","3C:BD:3E:C0:F8:BC"]

mac_id_cris = "de:c4:53:4c:d5:04"
mac_id_raul = "c3:09:89:ed:66:de"
mac_id_cris_car = "ea:d5:67:64:e1:67"
mac_id_tag_black = "ff:ff:00:05:da:ae"

mac_id_list = []
mac_id_list.append(mac_id_cris)
mac_id_list.append(mac_id_raul)
mac_id_list.append(mac_id_cris_car)
mac_id_list.append(mac_id_tag_black)

client= paho.Client("PresenceDetectionNode")
print("connecting to broker ")
client.connect("localhost",1883)#connect
client.loop_start() #start loop to process received messages

def parse_scan_message(scan_message):


    splitted_message = scan_message.split(";");
    mac_addr = splitted_message[1]
    rssi = splitted_message[4]
    mac_addr = mac_addr.strip()
    splitted_rssi = rssi.split(":")
    rssi = splitted_rssi[1]
    rssi = rssi.replace('>', '')
    rssi = int(rssi.strip())

    #rssi = int(rssi)
    #print(mac_addr)
    #print(rssi)

    result = [mac_addr,rssi]

    return result

def publish_message(mac_id, rssi):

    if(mac_id == mac_id_cris):
        print("Publishing message Cris")
        client.publish("presence_detection/cristina",rssi)
    elif(mac_id == mac_id_raul):
        print("Publishing message Raul")
        client.publish("presence_detection/raul",rssi)

    elif(mac_id == mac_id_cris_car):
        print("Publishing message Guest")
        client.publish("presence_detection/guest",rssi)

def find_mac_id(message, previous_results):

    parsed_message = parse_scan_message(message)
    count = 0
    for mac_id in mac_id_list:

        if(parsed_message[0] == mac_id and previous_results[count] == 0):
            print("Found device: " + mac_id + " RSSI: " + str(parsed_message[1]))
            previous_results[count] = 1
            publish_message(mac_id,parsed_message[1])

        count += 1

if __name__== "__main__":




    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        print("ble thread started")
    except:
        print("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    num_scans = 10
    previous_results = [0,0,0,0]
    while (num_scans > 0):
        returnedList = blescan.parse_events(sock, 10)
        #print("Scan")
        for beacon in returnedList:
            find_mac_id(str(beacon),previous_results)

        #sleep(0.1)
        num_scans -= 1

    print("Finished scan")
