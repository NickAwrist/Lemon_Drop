import subprocess

SSID2 = "JEREMYDASHCAM"
password2 = "4b8aydy2"

SSID3 = "VIOFO-A129P-124fc8"
password3 = "feb63688"

def connect_wifi(SSID, password):
    try:
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
    
def disconnect_wifi():
    try:
        disconnect_command = ["sudo", "nmcli", "dev", "disconnect", "wlan0"]
        result = subprocess.run(disconnect_command, check=True, capture_output=True, text=True)
        print("Wi-Fi disconnected successfully")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to disconnect Wi-Fi")
        print(e.stderr)
        
def check_wifi_connection():
    try:
        # Use nmcli to check the status of wlan0
        connection_command = ["nmcli", "-t", "-f", "DEVICE,STATE", "dev"]
        result = subprocess.run(connection_command, capture_output=True, text=True, check=True)
        
        # Look for wlan0 in the output
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