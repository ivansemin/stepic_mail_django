# -*- coding: utf-8 -*-

import time

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404, HttpResponseRedirect, redirect


from models import Question, Answer
from forms import AskForm, AnswerForm, SignupForm, LoginForm


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def post_list_all(request):
    questions = Question.objects.all().order_by('-added_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    paginator.baseurl = '/?page='
    page = paginator.page(page) # Page
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })

def popular(request):
    questions = Question.objects.all().order_by('-rating')
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page) # Page
    return render(request, 'popular.html', {
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })

def question(request, question_id):
    try:
        q = Question.objects.get(id=question_id)
    except ObjectDoesNotExist, err:
        raise Http404()

    answers = Answer.objects.filter(question=q)[:]
    form = AnswerForm()
    return render(request, 'question.html', {
        'answers': answers,
        'question': q,
        'form': form
    })

def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            user_id = request.COOKIES['sessionid']
            question = form.save(user_id)
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {
        'form': form
    })

def answer(request):
    if request.method == "POST":
        form = AnswerForm(request.POST)

        print form.data
        if form.is_valid():
            user_id = request.COOKIES['sessionid']
            answer = form.save(user_id)
            url = answer.get_url()
            print url
            return HttpResponseRedirect(url)
        else:
            raise Http404
            # return HttpResponseRedirect(reverse('question'), [question_id])
    else:
        raise Http404


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            response = redirect(reverse('home'))
            response.set_cookie('sessionid', user.id)
            return response
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form
    })


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                response = redirect(reverse('home'))
                response.set_cookie('sessionid', user.id)
                return response
            except ObjectDoesNotExist:
                pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form
    })