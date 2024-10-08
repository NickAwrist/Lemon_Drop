from flask import Flask, request, jsonify, Response
import os
import json
from wifi_controls import connect_wifi, disconnect_wifi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/add-connection', methods=['POST'])
def add_connection():
    data = request.get_json()
    if(os.path.exists('config.json')):
        with open('config.json', 'r') as config_file:
            load = json.load(config_file)
            
            if(data in load['connections']):
                return_json = {
                    "error" : "Connection already exists"
                }
                return return_json
            
            load['connections'].append(data)

        with open('config.json', 'w') as config_file:
            json.dump(load, config_file, indent=4)
        
        return_json = {
            "error":""
        }
        
    else:
        return_json = {
            "error":"config.json file does not exist"
        }
    
    return (return_json)

@app.route('/delete-connection', methods=['DELETE'])
def delete_connection():
    data = request.get_json()
    
    ssid = data['SSID']
    password = data['password']
    
    if(os.path.exists('config.json')):
        with open('config.json', 'r') as config_file:
            try:
                load = json.load(config_file)
                connections = load['connections']
                
                # This gets the first item from the list that matches the condition, 
                # and returns None if no item matches. (https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi)
                # matched = next((x for x in connections if x['SSID'] == ssid), None)
                
                matched_index = connections.index(data)
                print(matched_index)
                
                del connections[matched_index]
            
                
                # del connections[matched]

                # del matched
                print(load)
                
            except:
                return_json = {
                    "error" : "Connection is not saved on device"
                }
                
                return return_json
            
        with open('config.json', 'w') as config_file:
            json.dump(load, config_file, indent=4)
        
        return_json = {
            "error": ""
        }
        
        
    else:
        return_json = {
            "error":"config.json file does not exist"
        }
    
    return (return_json)
    
    
@app.route('/connect', methods=['POST'])
def connect():
    data = request.get_json()
    
    ssid = data['SSID']
    password = data['password']
    
    if(not connect_wifi(ssid, password)):
        return_json = {
            "error": "Connection failed"
        }
        return return_json, 400
    
    return_json = {
        "message": "Connected to ${ssid}"
    }
    
    return return_json, 201
    

@app.route('/disconnect', methods=['POST'])
def disconnect():
    
    disconnect_wifi()
    
    return_json = {
        "message": "Ended connection"
    }
    
    return return_json, 201
    

@app.route('/init-filebrowser', methods=['GET'])
def init_filebrowser():
    nice = os.system('filebrowser -d /home/lemon/Lemon_Drop/filebrowser -r /home/lemon/Lemon_Drop/videos -p 8080 -a 0.0.0.0')
    # connect_command = ["filebrowser", "-d", "/home/lemon/Lemon_Drop/filebrowser", "-r", "/home/lemon/Lemon_Drop/videos", "-p", "8080", "-a", "0.0.0.0"]
    # result = subprocess.run(connect_command, check=True, capture_output=True, text=True)
    
    
    return_json = {
        "message": "File browser started"
    }
    
    return return_json, 201

if __name__ == "__main__":
    app.run(debug=True)