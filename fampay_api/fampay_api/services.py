import sqlite3

from django.http import JsonResponse
from django.core.paginator import Paginator

from app.models import Youtube
from fampay_api.serializer import YoutubeSerializer


def get_videos(request):
    """
        GET API to get all the stored videos in the DB
        url = get/?page=1
    """
    page = int(request.GET.get('page'))
    try:
        search_results = Youtube.objects.all().order_by("-published_at")

        #pagination of the results
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page)

        #serialization
        serialized_results = YoutubeSerializer(page_obj.object_list, many=True)

        return JsonResponse({"result": serialized_results.data, "total_page": paginator.num_pages})
    except Exception as e:
        print(e)
        return JsonResponse({"result": "failed", "error": e})


def search_videos(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    """
        SEARCH API to get all the stored videos in the DB that matches the search query to title and description
        url = get/?query=q&page=1
    """
    search_query = request.GET.get('query')
    page = int(request.GET.get('page'))

    #making the query adequate for using in the SQL statement
    split_query = search_query.split(" ")
    search_query = '%'.join(split_query)

    column_name = ['video_id', 'title', 'description', 'published_at', 'thumbnail_url']
    try:
        # optimised search query

        cur.execute('SELECT video_id, title, description, published_at, thumbnail_url from app_youtube WHERE '
                    'title_description LIKE ?',
                                    ('%' + search_query + '%',))
        search_results = cur.fetchall()

        #formatting the output 
        formatted_result = [{field: value for field, value in zip(column_name, i)} for i in search_results]
        return JsonResponse({"result": formatted_result})
    except Exception as e:
        print(e)
        return JsonResponse({"result": "failed", "error": e})



