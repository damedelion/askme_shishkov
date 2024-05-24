from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from app.models import *
from app.forms import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_protect
import json

# Create your views here.

def paginate(objects_list, request, per_page=10):
  page_num = request.GET.get('page', 1)
  paginator = Paginator(objects_list, per_page)
  try:
    page = paginator.page(page_num)
  except (PageNotAnInteger, EmptyPage):
    page = paginator.page(1)

  return page

def index(request):
  page_obj = paginate(Question.objects.get_new(), request)
  context = {"questions": page_obj}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "index.html", context)

def hot(request):
  page_obj = paginate(Question.objects.get_hot(), request)
  context =  {"questions": page_obj}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "hot.html", context)

@login_required(login_url='login')
@csrf_protect
def question(request, question_id):
  item=Question.objects.get(pk=question_id)
  page_obj = paginate(Answer.objects.get_best(item), request)

  if request.method == 'GET':
    answer_form = AnswerForm()
  if request.method == 'POST':
    answer_form = AnswerForm(data=request.POST)
    if answer_form.is_valid():
      answer_form.save(item, request.user)
      return redirect(request.get_full_path())
      
  context = {"question": item, "answers": page_obj, "form": answer_form}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "question_detail.html", context)

def tag(request, tag):
  item=Tag.objects.get(name=tag)
  page_obj = paginate(Question.objects.get_by_tag(item), request)
  context = {"questions": page_obj, "tag": tag}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "tag.html", context)

def sign_up(request):
  if request.method == 'GET':
    signup_form = SignupForm()
  if request.method == 'POST':
    signup_form = SignupForm(request.POST, request.FILES)
    if signup_form.is_valid():
      user = signup_form.save()
      if user:
        return redirect(reverse('login'))
      
  context={'form': signup_form}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "signup.html", context)

@require_http_methods(['GET', 'POST'])
@csrf_protect
def log_in(request):
  if request.method == 'GET':
    login_form = LoginForm()
  if request.method == 'POST':
    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
      user = authenticate(request, **login_form.cleaned_data)
      login(request, user)
      return redirect(reverse('index'))    
    
  context={'form': login_form}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "login.html", context)

def log_out(request):
  logout(request)
  return redirect(reverse('login'))

@login_required(login_url='login')
@csrf_protect
def ask(request):
  if request.method == 'GET':
    ask_form = AskForm()
  if request.method == 'POST':
    ask_form = AskForm(data=request.POST)
    if ask_form.is_valid():
      question = ask_form.save(request.user)
      return redirect('question', question_id=question.pk)
    
  context={'form': ask_form}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "ask.html", context)

@login_required(login_url='login')
@csrf_protect
def settings(request):
  if request.method == 'GET':
    settings_form = SettingsForm()
  if request.method == 'POST':
    settings_form = SettingsForm(request.POST, request.FILES)
    if settings_form.is_valid():
      settings_form.save(request.user)

  context={'form': settings_form}
  if request.user.is_authenticated:
    context['profile'] = Profile.objects.get(user=request.user)
  return render(request, "settings.html", context)

@require_http_methods(["POST"])
@login_required(login_url='login')
@csrf_protect
def like_question(request, question_id):
  body = json.loads(request.body)
  question = get_object_or_404(Question, pk=question_id)
  profile = Profile.objects.get(user=request.user)
  question_like, question_like_created = QuestionLike.objects.get_or_create(is_liked=True, question=question, user=profile)

  if not question_like_created:
      question_like.delete()

  body['likes_count'] = QuestionLike.objects.filter(question=question).count()

  return JsonResponse(body)


@require_http_methods(["POST"])
@login_required(login_url='login')
@csrf_protect
def like_answer(request, answer_id):
  body = json.loads(request.body)
  answer = get_object_or_404(Answer, pk=answer_id)
  profile = Profile.objects.get(user=request.user)
  answer_like, answer_like_created = AnswerLike.objects.get_or_create(is_liked=True, answer=answer, user=profile)

  if not answer_like_created:
      answer_like.delete()

  body['likes_count'] = AnswerLike.objects.filter(answer=answer).count()

  return JsonResponse(body)
