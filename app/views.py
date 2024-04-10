from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Answer

# Create your views here.
QUESTIONS = Question.objects.all()

ANSWERS = Answer.objects.all()

def paginate(objects_list, request, per_page=10):
  page_num = request.GET.get('page', 1)
  paginator = Paginator(QUESTIONS, per_page)
  try:
    page = paginator.page(page_num)
  except (PageNotAnInteger, EmptyPage):
    page = paginator.page(1)

  return page

def index(request):
  page_obj = paginate(QUESTIONS, request)
  return render(request, "index.html", {"questions": page_obj})

def hot(request):
  page_obj = paginate(QUESTIONS, request)
  return render(request, "hot.html", {"questions": page_obj})

def question(request, question_id):
  item = QUESTIONS[question_id]
  page_obj = paginate(ANSWERS, request)
  return render(request, "question_detail.html", {"question": item, "answers": page_obj})

def tag(request, tag):
  page_obj = paginate(QUESTIONS, request)
  return render(request, "tag.html", {"questions": page_obj, "tag": tag})

def signup(request):
  return render(request, "signup.html")

def login(request):
  return render(request, "login.html")

def ask(request):
  return render(request, "ask.html")

def settings(request):
  return render(request, "settings.html")