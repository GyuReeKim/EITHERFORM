from django.shortcuts import render

# Create your views here.
def index(request):
    # 나중에 있을 충돌을 방지하기 위해 templates 안에 폴더를 따로 만들어준다.
    return render(request, 'questions/index.html')