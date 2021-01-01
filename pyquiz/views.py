from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    """
    pyquiz 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date') # 질문목록 데이터//작성일시 역순

    # 페이징처리
    paginator = Paginator(question_list, 10) # 페이지당 1개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}

    return render(request, 'pyquiz/question_list.html', context)

def detail(request, question_id):
    """
    pyquiz 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pyquiz/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pyquiz 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pyquiz:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pyquiz/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    """
    pyquiz 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pyquiz:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pyquiz/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pyquiz 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pyquiz:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pyquiz:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pyquiz/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pyquiz 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pyquiz:detail', question_id=question.id)
    question.delete()
    return redirect('pyquiz:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pyquiz 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pyquiz:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pyquiz:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pyquiz/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pyquiz 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pyquiz:detail', question_id=answer.question.id)