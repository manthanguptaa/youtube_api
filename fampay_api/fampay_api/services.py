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

