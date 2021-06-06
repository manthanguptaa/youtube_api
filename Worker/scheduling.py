from fetch_youtube_metadata import get_video_metadata
import time

period = 300

if __name__ == "__main__":
    while True:
        get_video_metadata(period)
        time.sleep(period)
