from instagrapi import Client
import os

def upload_instagram(video_path, caption, config):
    username = config.get("username")
    password = config.get("password")

    if not username or not password:
        return "Error: Missing Username or Password"

    try:
        cl = Client()
        cl.login(username, password)
        
        # Upload as Reel
        cl.clip_upload(video_path, caption)
        return "Success"
    except Exception as e:
        return f"Failed: {str(e)}"
