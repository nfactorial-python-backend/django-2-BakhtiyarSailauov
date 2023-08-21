from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path('', views.get_news, name='news'),
    path("<int:news_id>/", views.get_page, name="get_page"),
    path("create_news/", views.NewsView.as_view(), name="create_news"),
    path("<int:news_id>/edit/", views.NewsEditView.as_view(), name="edit_news"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("<int:news_id>/delete", views.delete_news, name="delete"),
    path("/<int:comment_id>/delete_comment/", views.delete_comment, name="delete_comment"),
    path("api/news", views.post_news_drf, name="post_news_drf"),
    path("api/news/<int:pk>", views.NewsDetailView.as_view(), name="news_detail_drf"),
    path("api/news/", views.NewsList.as_view(), name="news_list_drf"),
]