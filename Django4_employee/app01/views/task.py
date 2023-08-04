from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def task_list(request):
    """ 任務列表 """
    return render(request, "task_list.html")

@csrf_exempt
def task_ajax(request):
    ### 透過ajax 獲得get
    print(request.GET)
    print(request.POST)
    return HttpResponse("Success")