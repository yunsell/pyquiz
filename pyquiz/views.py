from django.shortcuts import render, get_object_or_404
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