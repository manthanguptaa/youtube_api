from fetch_youtube_metadata import get_video_metadata
import time
import requests

period = 10

if __name__ == "__main__":
    while True:
        try:
            get_video_metadata(period)
            time.sleep(period)
            print("RUN")
        except Exception as e:
            m = str(e)
        else:
            m = "RAN"
        finally:
            requests.post(url="https://hooks.slack.com/services/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", json = {'text':m})
