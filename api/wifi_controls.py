import subprocess
import os

def filebrowser_i():
    os.system('filebrowser -d /home/lemon/Lemon_Drop/filebrowser -r /home/lemon/Lemon_Drop/videos -p 8080 -a 0.0.0.0')

# Connect to the wifi givven an SSD and password
def connect_wifi(SSID, password):
    try:
        # Use nmcli to connect to the Wi-Fi network
        print(f"Connecting to {SSID}")
        
        connect_command = ["sudo", "nmcli", "dev", "wifi", "connect", SSID, "password", password]
        result = subprocess.run(connect_command, check=True, capture_output=True, text=True)
        
        print(f"Successfully connected to {SSID}")
        print(result.stdout)
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {SSID}")
        print(e.stderr)
        
        return False
    
# Disconnect from the wifi
def disconnect_wifi():
    try:
        # Use nmcli to disconnect from the Wi-Fi network
        disconnect_command = ["sudo", "nmcli", "dev", "disconnect", "wlan0"]
        result = subprocess.run(disconnect_command, check=True, capture_output=True, text=True)
       
        print("Wi-Fi disconnected successfully")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("Failed to disconnect Wi-Fi")
        print(e.stderr)
     
# Check if the wifi is connected   
def check_wifi_connection():
    try:
        # Use nmcli to check the connection status of wlan0
        connection_command = ["nmcli", "-t", "-f", "DEVICE,STATE", "dev"]
        result = subprocess.run(connection_command, capture_output=True, text=True, check=True)
        
        # Check the output of the command to see if wlan0 is connected or not
        for line in result.stdout.splitlines():
            if "wlan0:connected" in line:
                print("wlan0 is connected to a Wi-Fi network")
                return True
            elif "wlan0:disconnected" in line:
                print("wlan0 is not connected to any Wi-Fi network")
                return False

    except subprocess.CalledProcessError as e:
        print("Failed to check the Wi-Fi connection")
        print(e.stderr)
        return False