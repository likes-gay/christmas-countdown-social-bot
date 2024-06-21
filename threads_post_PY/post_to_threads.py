import os, time
import requests

THREADS_USER_ID = os.getenv("THREADS_USER_ID")
THREADS_ACSESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")

IMAGE_URL = "https://xmas-countdown.likes.gay/currentImage.png"
ENDPOINT = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}"

#WORK IN PROGRESS - https://developers.facebook.com/docs/threads/posts#single-thread-posts

def create_media_container():
    response = requests.post(f"{ENDPOINT}/threads",
                             params={
                                 "image_url": IMAGE_URL,
                                 "media_type": "IMAGE",
                                 "access_token": THREADS_ACSESS_TOKEN,
                             },
                             timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to create media container: {response.json()}")
    
    return response.json()["id"]

def publish_media_container(media_id):
    response = requests.post(f"{ENDPOINT}/threads_publish",
                             params={
                                 "creation_id": media_id,
                                 "access_token": THREADS_ACSESS_TOKEN
                             },
                             timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to publish media container: {response.json()}")
    
    return response.json()

media_container_id = create_media_container()

time.sleep(30)
# "It is recommended to wait on average 30 seconds before publishing a Threads media container
# to give our server enough time to fully process the upload."

publish_media_container(media_container_id)
