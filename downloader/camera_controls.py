import requests
import os
import xmltodict
import downloader.utils.commands as commands

BASE_URL = 'http://192.168.1.254'
BASE_COMMAND_URL = "http://192.168.1.254/?custom=1&cmd="


def get_battery_level():
    response = requests.get(BASE_COMMAND_URL + str(commands.GET_BATTERY_LEVEL))
    if(response.content == None):
        print('Error ' + str(response.status_code))
        exit(1)
                
    parsed_response = xmltodict.parse(response.content)
    battery_level = parsed_response['Function']['Value']

    return battery_level    


def get_all_videos():
    # get the list of all the file names needing to be downloaded
    response = requests.get(BASE_COMMAND_URL + str(commands.GET_FILE_LIST))
    if(response.content == None):
        print('Error: ' + str(response.status_code))
        exit()
    # print(response.headers)

    file_names = xmltodict.parse(response.content)

    i = 0
    for file in file_names['LIST']['ALLFile']:
        
        if ( i >= 20):
            break
        
        videoname = file['File']['NAME']
        
        if(os.path.exists(os.getcwd() + '/videos') == False):
            os.mkdir(os.getcwd() + '/videos')
        
        with open(('videos/' + str(videoname)), 'wb') as video_file:
            video_file.write(response.content)
        
        i += 1
        