from downloader.utils.wifi_connection import *
from downloader.camera_controls import *
import json
import os

from time import sleep

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
    
    
    print(f"Here are the current connections:")
    currently_connected = check_wifi_connection()
    if currently_connected is False:
        print("No active connections")
    else:
        print("Would you like to disconnect from the current connection? (y/n)")
        response = input()
        if response.lower() == 'y':
            disconnect_wifi()
    
    print("Making a new connection")
    config = load_config()
    print(f"Which connection would you like to make? (Number on the left)")
    
    c=1
    for connection in config['connections']:
        print(f"{c}: {connection['SSID']}")
        c+=1
    
    print(f"{c}: Exit")
    
    SSID_index = int(input())-1
    
    if SSID_index == len(config['connections']):
        print("Exiting")
        exit(0)
    
    SSID = config['connections'][SSID_index]['SSID']
    password = config['connections'][SSID_index]['password']
    
    print('SSID:' + SSID)
    print('password' + password)
    
    result = connect_wifi(SSID, password)
    
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