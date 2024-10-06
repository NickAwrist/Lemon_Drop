import requests
import os
import xmltodict
import downloader.utils.commands as commands
#wget        http://192.168.1.254/DCIM/Movie/20241005224959_023982.MP4
#            http://192.168.1.254/DCIM/Movie/20231003081810_000197.MP4
BASE_URL = 'http://192.168.1.254'
BASE_COMMAND_URL = "http://192.168.1.254/?custom=1&cmd="

# This will always return an XML response object
def request_command(command):
    response = requests.get(BASE_COMMAND_URL + str(command))
    if(response.content == None):
        print( 'Error Status: '+ str(response.status_code))
        print('\n')
        exit()
    return response

def request_movie(movie_name):
    
    response = requests.get(BASE_URL + '/DCIM/Movie/' + movie_name, allow_redirects=True)
    
    if response.status_code != 200:
        print('Error Status: ' + str(response.status_code))
        print('Failed to retrieve movie: ' + str(movie_name))
        exit()
    
    return response


def beep():
    # beep 10 times
    for i in range(10):
        b = request_command(commands.BEEP)
        print(xmltodict.parse(b.content))
        
def get_card_free_space():
    response =  request_command(commands.CARD_FREE_SPACE)
    return int(xmltodict.parse(response.content)["Function"]["Value"])/1000
        
# get list of all file names
def get_file_list():
    request =  request_command(commands.GET_FILE_LIST)
    file_list = xmltodict.parse(request.content)["LIST"]["ALLFile"]
    return file_list
    
def get_one_video(video_name):
    response = request_movie(video_name)
    return response.content
          
def get_all_videos():
    # get the list of all the file names needing to be downloaded
    response = request_command(commands.GET_FILE_LIST)

    file_names = xmltodict.parse(response.content)

    i = 0
    for file in file_names['LIST']['ALLFile']:
        
        if ( i >= 20):
            break
        
        videoname = file['File']['NAME']
        
        if(os.path.exists(os.getcwd() + '/videos') == False):
            os.mkdir(os.getcwd() + '/videos')
          
            
        video_response = request_movie(videoname)
        
        print(video_response)

        
        if video_response.status_code == 200:  
            with open(('videos/' + str(videoname)), 'wb') as video_file:
                video_file.write(video_response.content) 
        else:
            print(f"Failed to download video: {videoname}")
        
        
        i += 1
        