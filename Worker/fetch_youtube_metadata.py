import requests
from datetime import datetime, timezone, timedelta
import json
import sqlite3

con = sqlite3.connect('fampay_api/db.sqlite3')
cur = con.cursor()

params_for_api = {
    'part': 'snippet',
    'maxResults': 50,
    'order': 'date',
    'search_query': 'music',
    'api_key': ''
}


def get_video_metadata(value):
    published_after = get_past_five_minute_timestamp(value)
    url = f"https://youtube.googleapis.com/youtube/v3/search?" \
          f"part={params_for_api['part']}&" \
          f"maxResults={params_for_api['maxResults']}&" \
          f"order={params_for_api['order']}&" \
          f"publishedAfter={published_after}&" \
          f"q={params_for_api['search_query']}&" \
          f"key={get_api_key()}"

    response = requests.get(url=url)

    if response.status_code == 200:
        response_json = response.json()['items']
        # If successfully able to fetch the response then push the data to DB
        video_metadata = []
        for item in range(len(response_json)):
            # If 'videoId' key is present in response_json then get all the required fields and store in an array
            if 'videoId' in response_json[item]['id']:
                video_id = response_json[item]['id']['videoId']
                title = response_json[item]['snippet']['title'].lower()
                description = response_json[item]['snippet']['description'].lower()
                published_at = response_json[item]['snippet']['publishedAt']
                thumbnail_url = response_json[item]['snippet']['thumbnails']['default']['url']

                #Removing all the special characters from title and description 

                title_description = title + " " + description
                title_description_without_special_chars = ""
                split_words = []
                for character in title_description:
                    if character.isalnum():
                        title_description_without_special_chars += character
                    elif character == " " and title_description_without_special_chars != "":
                        split_words.append(title_description_without_special_chars)
                        title_description_without_special_chars = ""
                split_words.append(title_description_without_special_chars)
                title_description_without_special_chars = " ".join(split_words)
                
                # pushing the response into an array for batch write
                video_metadata.append((video_id, title, description, published_at, thumbnail_url, title_description_without_special_chars))

        try:
            # batch write all the data to the SQL DB in one go which makes it cheaper and faster
            cur.executemany(
                '''INSERT INTO app_youtube (video_id,title,description,published_at,thumbnail_url,title_description) 
                VALUES (?,?,?, ?,?,?)''',
                video_metadata)
            con.commit()
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print(e)


def get_api_key():
    return params_for_api['api_key']


def get_past_five_minute_timestamp(value):
    utc_past_hour = datetime.utcnow() + timedelta(seconds=-value)
    my_time = str(utc_past_hour.replace(tzinfo=timezone.utc)).split(' ')
    return f"{my_time[0]}T{my_time[1][:-6]}Z"
