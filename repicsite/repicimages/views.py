from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
from .forms import SplashFilter

links_per_page = 6

def index(request):

    '''
    DATABASE INTEGRATION
    :param request:
    :return links to display:
    '''

    links = ['www.google.com'] # placesavr for testing

    page = request.GET.get('page', 1)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request,'index.html', {'links': numbers})


def random(request):

    '''
    DATABASE INTEGRATION
    :param request:
    :return links to display:
    '''

    links = ['www.google.com'] # placesavr for testing

    randomizer = randint(1,int((len(links)/links_per_page)))
    page = request.GET.get('page', randomizer)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request,'index.html', {'links':numbers})


def splash(request):
    splash_filter = SplashFilter(request.POST)

    context = {'filter': splash_filter}
    return render(request,'splash.html',context)