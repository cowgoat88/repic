from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
from .forms import SplashFilter, NsfwAllow, FilterAll, NsfwOnlyFilter, FilterAllSafe, picsFilter, gifsFilter, funnyFilter, wildFilter
from scrap.models import Submission, SubredditsList

links_per_page = 5

def images(request):
    print(request.POST.getlist('choice_field'))

    splash_filter = SplashFilter(request.POST)
    all_filter = FilterAll(request.POST)
    all_safe = FilterAllSafe(request.POST)
    nsfw_filter = NsfwAllow(request.POST)
    nsfw_only_filter = NsfwOnlyFilter(request.POST)


    if request.method == "GET":
        if request.GET.get('page'):
            subreddits = request.GET.get('subreddits')
            subreddits = [str(x) for x in subreddits.split('!')]
            links = Submission.objects.filter(subredditid__in=subreddits).order_by('-score')[:50]
            page = request.GET.get('page')
            paginator = Paginator(links, links_per_page)
            try:
                numbers = paginator.page(page)
            except PageNotAnInteger:
                numbers = paginator.page(1)
            except EmptyPage:
                numbers = paginator.page(paginator.num_pages)

            return render(request, 'images.html', {'links': numbers, 'subreddits': '!'.join([str(x) for x in subreddits])})
        else:
            context = {'nsfw_filter': nsfw_filter, 'filter': splash_filter}
            return render(request, 'splash.html', context)

    elif request.method == "POST":
        print(request.POST.getlist('nsfw_field'))
        print(request.POST.getlist('choice_field'))
        if 'allow' in request.POST.getlist('nsfw_field'):
            context = {'nsfw_filter': False, 'filter': all_filter}
            return render(request, 'splash.html', context)
        elif 'only' in request.POST.getlist('nsfw_field'):
            context = {'nsfw_filter': False, 'filter': nsfw_only_filter}
            return render(request, 'splash.html', context)
        elif 'all' in request.POST.getlist('nsfw_field'):
            context = {'nsfw_filter': False, 'filter': all_safe}
            return render(request, 'splash.html', context)
        else:
            request.POST.getlist('choice_field')
            subreddits = request.POST.getlist('choice_field')
            links = Submission.objects.filter(subredditid__in=subreddits).order_by('-score')[:50]
            subreddits = '!'.join(subreddits)

            page = request.GET.get('page', 1)
            paginator = Paginator(links, links_per_page)
            try:
                numbers = paginator.page(page)
            except PageNotAnInteger:
                numbers = paginator.page(1)
            except EmptyPage:
                numbers = paginator.page(paginator.num_pages)
            return render(request, 'images.html', {'links': numbers, 'subreddits': subreddits})


    return 'dummy face'

def nsfw(request):
    all_filter = FilterAll(request.POST)
    context = {'nsfw_filter': False, 'filter': all_filter}
    return render(request, 'splash.html', context)

def all(request):
    all_safe = FilterAllSafe(request.POST)
    context = {'nsfw_filter': False, 'filter': all_safe}
    return render(request, 'splash.html', context)

def pics(request):
    subreddits = ['44','45','56','69']
    links = Submission.objects.filter(subredditid__in=subreddits).order_by('-score')[:50]
    subreddits = '!'.join(subreddits)

    page = request.GET.get('page', 1)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'images.html', {'links': numbers, 'subreddits': subreddits})

def gifs(request):
    subreddits = ['16','20','22','30','38']
    links = Submission.objects.filter(subredditid__in=subreddits).order_by('-score')[:50]
    subreddits = '!'.join(subreddits)

    page = request.GET.get('page', 1)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'images.html', {'links': numbers, 'subreddits': subreddits})

def funny(request):
    subreddits = ['36','37','26','20','46','49']
    links = Submission.objects.filter(subredditid__in=subreddits).order_by('-score')[:50]
    subreddits = '!'.join(subreddits)

    page = request.GET.get('page', 1)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'images.html', {'links': numbers, 'subreddits': subreddits})

def wild(request):
    subreddits = ['27','39','52','55']
    links = Submission.objects.filter(subredditid__in=subreddits).order_by('-score')[:50]
    subreddits = '!'.join(subreddits)

    page = request.GET.get('page', 1)
    paginator = Paginator(links, links_per_page)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'images.html', {'links': numbers, 'subreddits': subreddits})
