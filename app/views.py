from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import *

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
  return render(request, "index.html", context)

def hot(request):
  page_obj = paginate(Question.objects.get_hot(), request)
  context =  {"questions": page_obj}
  return render(request, "hot.html", context)

def question(request, question_id):
  item=Question.objects.get(pk=question_id)
  page_obj = paginate(Answer.objects.get_best(item), request)
  context = {"question": item, "answers": page_obj}
  return render(request, "question_detail.html", context)

""" def question_tags(request, question):
    return render(request, 'question.html', {'tags': Tag.objects.filter(question=question)}) """

def tag(request, tag):
  item=Tag.objects.get(name=tag)
  page_obj = paginate(Question.objects.get_by_tag(item), request)
  context = {"questions": page_obj, "tag": tag}
  return render(request, "tag.html", context)

def signup(request):
  return render(request, "signup.html")

def login(request):
  return render(request, "login.html")

def ask(request):
  return render(request, "ask.html")

def settings(request):
  return render(request, "settings.html")