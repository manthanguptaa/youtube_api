# Backend Assignment
> Make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Tech Stack
1. Django
2. DB - sqlite3 (inbuilt)

## DB Schema
![Untitled](https://user-images.githubusercontent.com/42516515/120895794-400f1600-c63c-11eb-860c-ff5135ac56e2.png)

## API Endpoints

1. GET API which returns the stored video data in a paginated response sorted in descending order of published datetime
    Access this endpoint by typing http://127.0.0.1:8000/get/?page=1
    Demo Output
    ![Screenshot from 2021-06-05 20-38-49](https://user-images.githubusercontent.com/42516515/120896207-2969be80-c63e-11eb-96c1-174686bc5bb6.png)

2. A basic search API to search the stored videos using their title and description (Optimised)
    Access this endpoint by typing http://127.0.0.1:8000/search/?query=india&page=1
    If you want to try different search queries then replace it with india. For more than 1 word concatenate them with '%20'. 
    Eg. Search Query = New Zealand then the endpoint will look like this http://127.0.0.1:8000/search/?query=new%20zealand&page=1
    Demo Output
    ![Screenshot from 2021-06-05 20-43-22](https://user-images.githubusercontent.com/42516515/120896343-b6147c80-c63e-11eb-9ca4-f069d50767fd.png)
5bb6.png)

**Note**: The default search query is for music. You can change it by going inside Worker folder and opening fetch_youtube_metadata.py file and change it on line 14.

## Setup

**Note**: Before moving forward please get your own API KEY from [here](https://console.cloud.google.com/apis/api/youtube.googleapis.com/). You can place this API KEY by going inside Worker folder and opening fetch_youtube_metadata.py file and change place it on line 15. Remember to place it inside quotes.

1. `git clone https://github.com/Manthan109/youtube_api.git`
2. `cd youtube_api`
3. `sudo docker build -t fampay .`
4. `sudo docker run -d -p 8000:8000 fampay`
5. And you are good to go! You can type in the endpoints and look at the results