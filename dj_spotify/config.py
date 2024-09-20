from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_NAME = os.getenv('USER_NAME')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')
PLAYLIST_NAME = os.getenv('PLAYLIST_NAME')