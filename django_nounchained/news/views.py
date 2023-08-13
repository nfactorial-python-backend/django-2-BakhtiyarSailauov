from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import News, Comments


def get_news(request):
    news = News.objects.order_by("-created_at")
    context = {"news": news}

    return render(request, "news/news.html", context)


def get_page(request, news_id):

    news = get_object_or_404(News, pk=news_id)

    content = request.POST.get('content')
    if content:
        comment = Comments(content=content, created_at=timezone.now(), News=news)
        comment.save()

    comments = Comments.objects.filter(News=news).order_by("-created_at")
    context = {"news": news, "comments": comments}
    return render(request, "news/page.html", context)


def create_news(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    if title and content:
        news = News(title=title, content=content, created_at=timezone.now())
        news.save()
        return HttpResponseRedirect(reverse("news:get_page", args=(news.id, )))

    return render(request, 'news/create_news.html')
