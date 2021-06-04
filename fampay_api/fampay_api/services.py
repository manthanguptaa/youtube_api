from django.http import JsonResponse

from fampay.models import Youtube
from django.core.paginator import Paginator

from fampay.serializer import YoutubeSerializer


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
    """
        SEARCH API to find all the matching title and description params
        url = search/?query=q&page=1
    """
    query = request.GET.get('query')
    page = int(request.GET.get('page'))
    try:
        search_results = Youtube.objects.filter(title__icontains=query,description__contains=query)\
            .order_by("-published_at")
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page)
        serialized_results = YoutubeSerializer(page_obj.object_list, many=True)

        return JsonResponse({"result": serialized_results.data, "total_page": paginator.num_pages})
    except Exception as e:
        print(e)
        return JsonResponse({"success": "failed", "result": e})
