from downloader.utils.wifi_connection import establish_wifi_connection
from downloader.camera_controls import *
import json
import os

from time import sleep

# config = {
#     "setup" : False,
    
#     "connections" : [
        
#         {"SSID":"Sevsung", "password":"12345678"},
#         {"SSID":"JEREMYDASHCAM", "password":"4b8aydy2"},
#         {"SSID":"VIOFO-A129P-124fc8", "password":"feb63688"}
#     ]
# }

config_path = "config.json"

def load_config():
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            try:
                config = json.load(config_file)
                print("Config loaded successfully.")
                return config
            except json.JSONDecodeError:
                print("Error: The configuration file is corrupted")
                exit(1)
    else:
        print("Error: config.json file not found")
        exit(1)
                    
def main():
    
    config = load_config()
    print(f"Which connection would you like to make? (Number on the left)")
    
    c=1
    for connection in config['connections']:
        print(f"{c}: {connection['SSID']}")
        c+=1
        
    SSID_index = int(input())-1
    
    SSID = config['connections'][SSID_index]['SSID']
    password = config['connections'][SSID_index]['password']
    
    print('SSID:' + SSID)
    print('password' + password)
    
    result = establish_wifi_connection(SSID, password)
    
    while result is False:
        print("Attempting to connect again in 15 seconds")
        sleep(15)
        result = establish_wifi_connection(SSID, password)
     
    
    battery_level = get_battery_level()
    print(f"{battery_level}") 
        
    #print("Fetching videos")
    # get_videos()
    
    
if __name__ == "__main__":
    main()