from downloader.utils.wifi_controls import *
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
            
# Connect to the first saved connection. If no connection is made, keeo trying.
# Our program only runs when there is a connection or an API endpoint is called (which needs a connection :O)
def connect():
    
    # Load config
    config = load_config()

    # Grab the first connection key value pair
    SSID_index = 0
    SSID = config['connections'][SSID_index]['SSID']
    password = config['connections'][SSID_index]['password']
    
    # Connect to the wifi
    result = connect_wifi(SSID, password)

    # If no connection is present, keep retryinh
    while result is False:
        print("Attempting to connect again in 15 seconds")
        sleep(15)
        result = connect_wifi(SSID, password)
                    
def main():
    
    # Search for a webcam connection
    connect()
    
    # Once a connection is established, retrieve the 15 most recent videos
    get_all_videos(limit=15)
    
    disconnect_wifi()
    
    # Wait 5 minutes
    sleep(5*60)
    
    # Cyrcle
    main()
    
if __name__ == "__main__":
    main()