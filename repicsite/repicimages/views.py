from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
from .forms import SplashFilter
from .models import Submission

links_per_page = 5

def images(request):

    '''
    DATABASE INTEGRATION
    :param request:
    :return links to display:
    '''
    splash_filter = SplashFilter(request.POST)

    if request.method == "GET":
        context = {'filter': splash_filter}
        return render(request, 'splash.html', context)

    elif request.method == "POST":
        print(request.POST.getlist('choice_field'))
        print(len(Submission.objects.filter(subreddit__in=request.POST.getlist('choice_field'))))
        links = Submission.objects.filter(subreddit__in=request.POST.getlist('choice_field'))
        page = request.GET.get('page', 1)
        paginator = Paginator(links, links_per_page)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)

        return render(request, 'images.html', {'links': numbers})

    links = ['google.com']
    page = request.GET.get('page', 1)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request,'splash.html', {'links': numbers, 'filter': splash_filter})


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
    if request.method == "POST":
        print(request.POST.getlist('choice_field'))
    context = {'filter': splash_filter}
    return render(request,'splash.html',context)