from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question


def index(request):
    """
    pyquiz 목록 출력
    """
    question_list = Question.objects.order_by('-create_date') # 질문목록 데이터//작성일시 역순
    context = {'question_list': question_list}
    return render(request, 'pyquiz/question_list.html', context)

def detail(request, question_id):
    """
    pyquiz 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pyquiz/question_detail.html', context)

def answer_create(request, question_id):
    """
    pyquiz 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pyquiz:detail', question_id=question.id)