from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path('', views.get_news, name='news'),
    path("<int:news_id>/", views.get_page, name="get_page"),
    path("create_news/", views.create_news, name="create_news")
]