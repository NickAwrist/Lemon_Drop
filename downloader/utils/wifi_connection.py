import subprocess

SSID2 = "JEREMYDASHCAM"
password2 = "4b8aydy2"

SSID3 = "VIOFO-A129P-124fc8"
password3 = "feb63688"

def establish_wifi_connection(SSID, password):
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