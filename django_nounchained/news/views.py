from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from .forms import NewsForm, SignUpForm
from .models import News, Comments
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


def get_news(request):
    news = News.objects.order_by("-created_at")
    user_is_moderator = request.user.groups.filter(name='moderators').exists()
    context = {"news": news,
               'user_is_moderator': user_is_moderator,
               }

    return render(request, "news/news.html", context)


def get_page(request, news_id):

    news = get_object_or_404(News, pk=news_id)
    user_is_moderator = request.user.groups.filter(name='moderators').exists()

    content = request.POST.get('content')
    if content:
        comment = Comments(author=request.user, content=content, created_at=timezone.now(), News=news)
        comment.save()

    comments = Comments.objects.filter(News=news).order_by("-created_at")
    context = {"news": news, "comments": comments, "user_is_moderator": user_is_moderator}
    return render(request, "news/page.html", context)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.method == "POST":
        if request.user == comment.author or request.user.groups.filter(name='moderators').exists():
            comment.delete()
        else:
            messages.error(request, 'У вас нет прав для удаления этого комментария.')

    return redirect(reverse("news:get_page", args=(comment.News.id, )))


class NewsView(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request):
        form = NewsForm()
        return render(request, 'news/create_news.html', {'form': form})

    @method_decorator(login_required(login_url="/login/"))
    @method_decorator(permission_required("news.add_news", login_url="/login/"))
    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return HttpResponseRedirect(reverse("news:get_page", args=(news.id, )))

        return render(request, 'news/create_news.html', {"form": form})


def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST":
        if request.user == news.author or request.user.groups.filter(name='moderators').exists():
            news.delete()
    return redirect(reverse("news:news"))


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


def sign_up(request):
    if request.method == "POST":
        print(request)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['moderator'] == True:
                group = Group.objects.get(name="moderators")
            else:
                group = Group.objects.get(name="default")

            group.user_set.add(user)
            login(request, user)
            return redirect(reverse("news:news"))
    else:
        form = SignUpForm()

    return render(request, "registration/sign_up.html", {"form": form})