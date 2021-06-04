import requests
from datetime import datetime, timezone, timedelta
import os
import json
import sqlite3

con = sqlite3.connect('../fampay_api/db.sqlite3')
cur = con.cursor()

params_for_api = {
    'part': 'snippet',
    'maxResults': 50,
    'order': 'date',
    'search_query': 'cricket',
    'api_key': 'AIzaSyBk8XcZpmQ61hmVvqK9AIHy3ImfYPC4V3I'
}


def get_video_metadata():
    url = f"https://youtube.googleapis.com/youtube/v3/search?" \
          f"part={params_for_api['part']}&" \
          f"maxResults={params_for_api['maxResults']}&" \
          f"order={params_for_api['order']}&" \
          f"q={params_for_api['search_query']}&" \
          f"key={get_api_key()}"
    print(url)
    response = requests.get(url=url)
    response_json = response.json()['items']

    if response.status_code == 200:
        # If successfully able to fetch the response then push the data to DB
        for item in range(len(response_json)):
            try:
                video_id = response_json[item]['id']['videoId']
                title = response_json[item]['snippet']['title']
                description = response_json[item]['snippet']['description']
                published_at = response_json[item]['snippet']['publishedAt']
                thumbnail_url = response_json[item]['snippet']['thumbnails']['default']['url']
                cur.execute(
                    '''INSERT INTO app_youtube (video_id,title,description,published_at,thumbnail_url) VALUES (?,?,?,?,?)''',
                    (video_id, title, description, published_at, thumbnail_url,))
                con.commit()
            except sqlite3.IntegrityError:
                pass
            except Exception as e:
                print(e)


def get_api_key():
    return params_for_api['api_key']


get_video_metadata()
