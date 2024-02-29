from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import *
from recommend.nn.prediction import net_music_list, net_recommend_genre, net_predict_music


@csrf_exempt
def recommendView(request):
    return render(request, 'recommend.html')


# 随机推荐5首歌曲
def get_music_list(request):
    music_list = net_music_list()
    return JsonResponse(music_list, safe=False)


# 返回随机推荐5首同种风格的歌曲
def get_recommend_genre(request):
    get_result = request.POST["album"]
    print(get_result + "=====================================================================================")
    music_list = net_recommend_genre(get_result)
    return JsonResponse(music_list, safe=False)


# 返回随机推荐5首喜欢的歌曲
def get_music_recommend(request):
    get_result = request.POST["musicIndex"]
    print(get_result + "=====================================================================================")
    music_list = net_predict_music(get_result)
    return JsonResponse(music_list, safe=False)
