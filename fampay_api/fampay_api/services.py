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
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page)
        serialized_results = YoutubeSerializer(page_obj.object_list, many=True)

        return JsonResponse({"result": serialized_results.data, "total_page": paginator.num_pages})
    except Exception as e:
        print(e)
        return JsonResponse({"success": "failed", "result": e})


def search_videos(request):
    con = sqlite3.connect('../db.sqlite3')
    cur = con.cursor()
    """
        SEARCH API to get all the stored videos in the DB that matches the search query to title and description
        url = get/?query=q&page=1
    """
    search_query = request.GET.get('query')
    page = int(request.GET.get('page'))
    split_query = search_query.split(" ")
    # search_query = "%".join(split_query)
    # print(split_query)
    # print(search_query)
    try:
        # cur.execute('SELECT name from sqlite_master where type= "table"')
        # paginator = Paginator(search_results, 25)
        # page_obj = paginator.get_page(page)
        # serialized_results = YoutubeSerializer(page_obj.object_list, many=True)
        # print(cur.fetchall())
        search_results = Youtube.objects.filter(title_description__icontains=search_query) \
            .order_by('-published_at')
        print(search_results.query)
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page)

        '''
        Serializing results using Django Rest Framework
        '''
        serialized_results = YoutubeSerializer(page_obj.object_list, many=True)

        return JsonResponse({"result": serialized_results.data, "total_page": paginator.num_pages})
        # return JsonResponse({"result": 'OK'})
    except Exception as e:
        print(e)
        return JsonResponse({"success": "failed", "result": e})



