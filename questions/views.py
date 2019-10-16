from django.shortcuts import render
from .forms import QuestionForm

# Create your views here.
def index(request):
    # 나중에 있을 충돌을 방지하기 위해 templates 안에 폴더를 따로 만들어준다.
    return render(request, 'questions/index.html')

def create(request):
    if request.method == "POST":
        pass
    else:
        form = QuestionForm()
        context = {
            'form': form,
        }
        return render(request, 'questions/form.html', context)
        # return render(request, 'questions/form.html', {'form': form,})