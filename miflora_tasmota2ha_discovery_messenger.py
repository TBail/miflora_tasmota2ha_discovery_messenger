import sys
import json
import argparse
import re
import os.path
import paho.mqtt.client as mqtt

from collections import OrderedDict


project_name = 'Mi Flora Tasmota 2 Homeassistant Discovery Messenger Tool'
project_url = 'https://github.com/tbail'

# Parse the commandline
parser = argparse.ArgumentParser(description=project_name, epilog='For further details see: ' + project_url)
parser.add_argument('--host', help='set name or ip of mqtt host. Defaults to "localhost"', default='localhost')
parser.add_argument('--port', help='set mqtt port. Defaults to "1883"', type=int, default=1883)
parser.add_argument('--user', help='set mqtt user. Defaults to "None"', default=None)
parser.add_argument('--pwd', help='set mqtt password. Defaults to "None"', default=None)
parser.add_argument('--mac', help='set mac address of the mi flora sensor to discover', default='112233445566')
parse_args = parser.parse_args()
mac = parse_args.mac.lower()
mac_suffix = mac[-6:]
mac_pretty = (':'.join(re.findall('..', mac))).upper()
mqtt_host = parse_args.host
mqtt_port = parse_args.port
mqtt_user = parse_args.user
mqtt_password = parse_args.pwd

print(project_name)
print('Source:', project_url)

print('Connecting to MQTT broker ...')
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_user, mqtt_password)
try:
    mqtt_client.connect(mqtt_host, port=mqtt_port, keepalive=60)
except:
    print(f'MQTT connection error. Please check your settings.')
    sys.exit(1)

# Discover temperature
topic = f'homeassistant/sensor/miflora_{mac}/temperature/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_temperature'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} Temperature'
payload['val_tpl'] ='{{value_json.Temperature}}'
payload['unit_of_meas'] = '°C'
payload['state_class'] = 'measurement'
payload['device_class'] = 'temperature'
payload['expire_after'] = '3600'
payload['dev'] = {
        'ids' : [f'miflora_{mac}'],
        'mf' : 'Xiaomi',
        'name' : f'Mi Flora {mac_pretty}',
        'mdl' : 'HHCCJCY01'}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: Temperature')

# Discover illuminance
topic = f'homeassistant/sensor/miflora_{mac}/illuminance/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_illuminance'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} Illuminance'
payload['val_tpl'] ='{{value_json.Illuminance}}'
payload['unit_of_meas'] = 'lx'
payload['state_class'] = 'measurement'
payload['device_class'] = 'illuminance'
payload['expire_after'] = '3600'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: Illuminance')

# Discover moisture
topic = f'homeassistant/sensor/miflora_{mac}/moisture/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_moisture'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} Moisture'
payload['val_tpl'] ='{{value_json.Moisture}}'
payload['unit_of_meas'] = '%'
payload['state_class'] = 'measurement'
payload['device_class'] = 'humidity'
payload['expire_after'] = '3600'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: Moisture')

# Discover fertility
topic = f'homeassistant/sensor/miflora_{mac}/fertility/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_fertility'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} Fertility'
payload['val_tpl'] ='{{value_json.Fertility}}'
payload['unit_of_meas'] = 'µs/cm'
payload['ic'] = 'mdi:leaf'
payload['state_class'] = 'measurement'
payload['expire_after'] = '3600'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: Fertility')

# Discover battery
topic = f'homeassistant/sensor/miflora_{mac}/battery/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_battery'
payload['ent_cat'] = 'diagnostic'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} Battery'
payload['val_tpl'] ='{{value_json.Battery}}'
payload['unit_of_meas'] = '%'
payload['device_class'] = 'battery'
payload['expire_after'] = '86400'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: Battery')

# Discover rssi
topic = f'homeassistant/sensor/miflora_{mac}/rssi/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_rssi'
payload['ent_cat'] = 'diagnostic'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} RSSI'
payload['val_tpl'] ='{{value_json.RSSI}}'
payload['unit_of_meas'] = 'dB'
payload['device_class'] = 'signal_strength'
payload['expire_after'] = '86400'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: RSSI')

# Discover mac
topic = f'homeassistant/sensor/miflora_{mac}/mac/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_mac'
payload['ent_cat'] = 'diagnostic'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} MAC'
payload['val_tpl'] ='{{value_json.mac}}'
payload['expire_after'] = '86400'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: MAC Address')

# Discover firmware
topic = f'homeassistant/sensor/miflora_{mac}/firmware/config'
payload = OrderedDict()
payload['~'] = f'tele/tasmota_ble'
payload['uniq_id'] = f'miflora_{mac}_firmware'
payload['ent_cat'] = 'diagnostic'
payload['stat_t'] = f'~/Flora{mac_suffix}'
payload['name'] = f'Mi Flora {mac_pretty} Firmware'
payload['val_tpl'] ='{{value_json.Firmware}}'
payload['expire_after'] = '86400'
payload['dev'] = {'ids' : [f'miflora_{mac}']}
mqtt_client.publish(topic, json.dumps(payload), 1, retain=True)
print(f'Published dicovery message: Firmware')

print(f'HA discovery messages for seneor {mac_pretty} send.')
 
