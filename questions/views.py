from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    questions = Question.objects.all()
    # 나중에 있을 충돌을 방지하기 위해 templates 안에 폴더를 따로 만들어준다.
    return render(request, 'questions/index.html', {'questions': questions})

def detail(request, id):
    question = get_object_or_404(Question, id=id)
    choice_form = ChoiceForm()

    choices = question.choice_set.all()

    total_1 = choices.filter(pick=1).count()
    total_2 = choices.filter(pick=2).count()
    
    total_sum = total_1 + total_2

    if total_sum == 0:
        percent_1 = 0
        percent_2 = 0
    else:
        percent_1 = total_1 / total_sum * 100
        percent_2 = total_2 / total_sum * 100

    context = {
        'question': question,
        'choice_form': choice_form,
        'percent_1': percent_1,
        'percent_2': percent_2,
    }
    return render(request, 'questions/detail.html', context)

def create(request):
    # 1. 사용자가 데이터를 입력하기 위해서 GET요청(폼을 요청)
    # 6. 사용자가 올바르지 않은 데이터를 입력하고 POST요청
    # 12. 사용자가 올바른 데이터를 입력하고 POST요청

    # 7. POST method로 들어오기 때문에 if문 실행
    # 13. POST method로 들어오기 때문에 if문 실행
    if request.method == "POST":
        # 8. 사용자의 데이터를 모델폼에 입력
        # 14. 사용자의 데이터를 모델폼에 입력
        form = QuestionForm(request.POST)
        # 9. 데이터가 올바른지 검증
        # 15. 데이터가 올바른지 검증
        if form.is_valid():
            # 16. 데이터가 검증을 통과하고 저장
            form.save()
            # 17. 저장 후 메인으로 이동
            return redirect('questions:index')
    # 2. GET method로 들어오기 때문에 else문 실행
    else:
        # 3. 사용자에게 빈 폼을 보여주기 위해서 모델폼을
        #    인스턴스화 한 후 form 변수에 저장
        form = QuestionForm()
    # 4. dict로 만들기
    # 10. 검증을 통과 못했을경우 => 올바른 데이터는 남기고 다시 폼 보여주기
    context = {
        'form': form,
    }
    # 5. form.html 보여주기
    # 11. form.html 보여주기
    return render(request, 'questions/form.html', context)

def update(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('questions:detail', id)
    else:
        form = QuestionForm(instance=question)
    context = {
        'form': form,
    }
    return render(request, 'questions/form.html', context)

def delete(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, id=id)
        question.delete()
        return redirect('questions:index')
    else:
        return redirect('questions:detail', id)

def choice_create(request, id):
    question = get_object_or_404(Question, id=id)
    choice_form = ChoiceForm(request.POST)
    if choice_form.is_valid():
        # 비어있는 값(question)이 있기 때문에 commit=False를 적어준다.
        choice = choice_form.save(commit=False)
        choice.question = question
        choice.save()
    return redirect('questions:detail', id)

    # question = get_object_or_404(Question, id=id)
    # if request.method == "POST":
    #     choice_form = ChoiceForm(request.POST)
    #     if choice_form.is_valid():
    #         # 비어있는 값(question)이 있기 때문에 commit=False를 적어준다.
    #         choice = choice_form.save(commit=False)
    #         choice.question = question
    #         choice.save()
    #         return redirect('questions:detail', id)
    # else:
    #     pass

# 이 decorator는 POST 요청만 받을 경우 사용한다. (GET 방식이 들어오지 않을 경우에 사용한다.) 405오류를 띄워준다.
@require_POST
def choice_delete(request, question_id, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    choice.delete()
    return redirect('questions:detail', question_id)

    # choice = get_object_or_404(Choice, id=choice_id)
    # if request.method == "POST":
    #     choice.delete()
    #     return redirect('questions:detail', question_id)
    # else:
    #     pass