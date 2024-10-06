from flask import Flask, request, jsonify, Response
import os
import json

app = Flask(__name__)

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
    
    



if __name__ == "__main__":
    app.run(debug=True)