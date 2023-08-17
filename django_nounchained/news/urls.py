from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path('', views.get_news, name='news'),
    path("<int:news_id>/", views.get_page, name="get_page"),
    path("create_news/", views.NewsView.as_view(), name="create_news"),
    path("<int:news_id>/edit/", views.NewsEditView.as_view(), name="edit_news"),
]