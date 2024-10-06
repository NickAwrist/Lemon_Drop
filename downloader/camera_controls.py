import requests
import os
import xmltodict
import subprocess
import concurrent.futures
import downloader.utils.commands as commands

BASE_URL = 'http://192.168.1.254'
BASE_COMMAND_URL = "http://192.168.1.254/?custom=1&cmd="
MAX_WORKERS = 4  # Adjust this based on your Raspberry Pi's capabilities

def request_command(command):
    response = requests.get(BASE_COMMAND_URL + str(command))
    if response.content is None:
        print('Error Status: ' + str(response.status_code))
        print('\n')
        exit()
    return response

def download_movie(movie_name):
    full_url = f"{BASE_URL}/DCIM/Movie/{movie_name}"
    output_path = os.path.join('videos', movie_name)
    
    try:
        subprocess.run([
            "curl", "-o", output_path, 
            "-C", "-",  # Resume partial downloads
            "--retry", "3",  # Retry up to 3 times
            "--retry-delay", "5",  # Wait 5 seconds between retries
            "-L",  # Follow redirects
            full_url
        ], check=True)
        print(f"Downloaded {movie_name} with curl")
        return True
    except subprocess.CalledProcessError as e:
        print(f"curl failed for {movie_name}: {e}")
        return False

def get_file_list():
    request = request_command(commands.GET_FILE_LIST)
    file_list = xmltodict.parse(request.content)["LIST"]["ALLFile"]
    return file_list

def get_all_videos(limit=None):
    file_list = get_file_list()
    
    # Sort files by date (assuming the filename contains the date)
    file_list.sort(key=lambda x: x['File']['NAME'], reverse=True)
    
    # Limit the number of files if specified
    if limit is not None:
        file_list = file_list[:limit]
    
    successful_downloads = 0
    failed_downloads = 0

    # Create the videos directory if it doesn't exist
    if not os.path.exists('videos'):
        os.mkdir('videos')

    # Use a ThreadPoolExecutor for parallel downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks
        future_to_movie = {executor.submit(download_movie, file['File']['NAME']): file['File']['NAME'] for file in file_list}
        
        # Process the results as they complete
        for future in concurrent.futures.as_completed(future_to_movie):
            movie_name = future_to_movie[future]
            try:
                if future.result():
                    successful_downloads += 1
                else:
                    failed_downloads += 1
            except Exception as exc:
                print(f'{movie_name} generated an exception: {exc}')
                failed_downloads += 1

    print(f"Download complete. Successfully downloaded: {successful_downloads}, Failed: {failed_downloads}")