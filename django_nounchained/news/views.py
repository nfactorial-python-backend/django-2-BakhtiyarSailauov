from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from .forms import NewsForm
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


class NewsView(View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'news/create_news.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            news.save()
            return HttpResponseRedirect(reverse("news:get_page", args=(news.id, )))

        return render(request, 'news/create_news.html', {"form": form})


class NewsEditView(View):
    def get(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = NewsForm(instance=news)
        return render(request, 'news/edit_news.html', {'form': form,
                                                       'news_id': news_id})

    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("news:get_page", args=(news_id, )))