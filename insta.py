import requests
 
class InstagramReelDownloader:
    """
    A class to handle the extraction and downloading of videos from Instagram reels.
    added some info into the documentation...
    """
 
    def __init__(self, reel_urls):
        """
        Initialize the downloader with a list of reel URLs.
        """
        self.reel_urls = reel_urls
 
    def modify_instagram_url(self, url):
        """
        Modify the original Instagram URL to access the JSON data.
        """
        try:
            split_url = url.split('/?', 1)
            modified_url = f"{split_url[0]}?__a=1&__d=dis"
            return modified_url
        except IndexError as e:
            print(f"Error modifying URL: {e}")
            return None
 
    def extract_video_url(self, json_url):
        """
        Extract the video URL from the JSON response of the Instagram reel.
        """
        try:
            response = requests.get(json_url)
            if response.status_code == 200:
                json_data = response.json()
                return json_data["graphql"]["shortcode_media"]["video_url"]
            else:
                print(f"Failed to fetch JSON data. Status code: {response.status_code}")
                return None
        except KeyError as e:
            print(f"Error extracting video URL from JSON: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
 
    def download_video(self, video_url, file_name):
        """
        Download the video from the given URL and save it to the specified filename.
        """
        try:
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print(f"Video downloaded successfully as {file_name}")
            else:
                print(f"Failed to download video. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading the video: {e}")
 
    def process_reels(self):
        """
        Process each reel URL: modify it, extract the video URL, and download the video.
        """
        for index, url in enumerate(self.reel_urls, start=1):
            print(f"\nProcessing Reel {index}: {url}")
 
            # Modify the URL to get JSON data
            json_url = self.modify_instagram_url(url)
            if not json_url:
                print("Skipping due to invalid URL format.")
                continue
 
            # Extract the video URL from the JSON response
            video_url = self.extract_video_url(json_url)
            if not video_url:
                print("Skipping due to missing or inaccessible video URL.")
                continue
 
             
            file_name = f'video_{index}.mp4'
            self.download_video(video_url, file_name)
 
  
if __name__ == "__main__":
    
    reel_urls = [
        "https://www.instagram.com/reel/DADPYeptu6l/?igsh=MTNpNHZxbzVzY2Rjbg==",
        "https://www.instagram.com/reel/DBSvLjCy7wF/?igsh=Y2lwanZqZ3Q4N2Rl",
        "https://www.instagram.com/reel/DBYVweXyMJ7/?igsh=NzAwZnRvaXNsZ2sx",
        "https://www.instagram.com/reel/C_VR8lnSl4H/?igsh=MXdteHM3eGZlNGowbw==",
        "https://www.instagram.com/reel/DABrNCcqjTu/?igsh=YXFtd25pZnI3ZXIx",
        "https://www.instagram.com/reel/DBX89-Nvfw0/?igsh=ZDBkNjBtMnd2Y2dh",
        "https://www.instagram.com/reel/DBRYSa4yPbX/?igsh=MXJwbzk5bXQ1MWZ1cw==",
        "https://www.instagram.com/reel/C_nIFhGyIjP/?igsh=MTNhaHg1bDFyMTZrYQ==",
        "https://www.instagram.com/reel/DBQ_GgAN6r_/?igsh=MTA3cDk3OHlzM25jeA==",
        "https://www.instagram.com/reel/DBQ9OLlsnnm/?igsh=czRkMzAyM2Vrcm9w"
    ]
 
     
    
    downloader = InstagramReelDownloader(reel_urls)
    downloader.process_reels()