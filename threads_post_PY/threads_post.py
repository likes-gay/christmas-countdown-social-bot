import os, time, requests
from PIL import Image
from refresh_key import extend_access_token

THREADS_USER_ID = os.getenv("THREADS_USER_ID")
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")

IMAGE_URL = "https://xmas-countdown.likes.gay/currentImage.png"
ENDPOINT = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}"

def create_media_container():
    #BytesIO(requests.get(IMAGE_URL).content
    metadata = Image.open("./currentImage.png").text
    
    response = requests.post(f"{ENDPOINT}/threads",
                            params={
                                "image_url": IMAGE_URL,
                                "media_type": "IMAGE",
                                "access_token": THREADS_ACCESS_TOKEN,
                                "alt_text": metadata["alt_text"],
                                "text": metadata["caption"],
                            },
                            timeout=30
    )
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to create media container: {response.json()}")
    
    return response.json()["id"]

def publish_media_container(media_id):
    response = requests.post(f"{ENDPOINT}/threads_publish",
                            params={
                                "creation_id": media_id,
                                "access_token": THREADS_ACCESS_TOKEN,
                                "fields": "permalink"
                            },
                            timeout=30
    )
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to publish media container: {response.json()}")
    
    return response.json()

media_container = create_media_container()

# "It is recommended to wait on average 30 seconds before publishing a Threads media container
# to give our server enough time to fully process the upload."
# https://developers.facebook.com/docs/threads/posts/#step-2--publish-a-threads-media-container
time.sleep(30)

publish_res = publish_media_container(media_container)
print(f"Post created!\nLink: {publish_res["permalink"]}")

extend_access_token(THREADS_ACCESS_TOKEN)