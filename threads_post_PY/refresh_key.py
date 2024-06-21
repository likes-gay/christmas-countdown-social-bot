import os
import requests

THREADS_API_URL = "https://graph.threads.net/"

def extend_access_token(THREADS_ACCESS_TOKEN):
    URL = f"{THREADS_API_URL}/refresh_access_token"
    
    r = requests.get(
        url=URL,
        params={
            "grant_type": "th_refresh_token",
            "access_token": THREADS_ACCESS_TOKEN,
        },
    )
    
    if r.status_code != 200:
        raise Exception(f"Failed to extend access token: {r.json()}")
    
    return r.json()["access_token"]


ACCSESS_TOKEN = input("Enter your Threads access token: ")

print(extend_access_token(ACCSESS_TOKEN))