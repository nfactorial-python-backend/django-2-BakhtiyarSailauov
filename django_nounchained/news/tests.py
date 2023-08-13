from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from datetime import timedelta
from .models import News, Comments


class NewsModelTests(TestCase):
    def test_has_comments_true(self):
        news = News(title="Срочно!", content="Отбор на nFactorial закрыто!", created_at=timezone.now())
        comment = Comments(content="Жаль(", created_at=timezone.now(), News=news)
        news.save()
        comment.save()
        self.assertIs(True, news.has_comments())

    def test_has_comments_false(self):
        news = News(title="Срочно!", content="Отбор на nFactorial открыто!", created_at=timezone.now())
        news.save()
        self.assertIs(False, news.has_comments())


class NewsViewTests(TestCase):
    def test_order_news(self):
        news1 = News(title="Срочно!", content="Отбор на nFactorial открыто!", created_at=timezone.now() + timedelta(hours=1))
        news2 = News(title="Не срочно!", content="Отбор на nFactorial все еще проходят!", created_at=timezone.now() + timedelta(hours=2))
        news3 = News(title="Очень срочно!", content="Отбор на nFactorial закрывается!", created_at=timezone.now() + timedelta(hours=3))

        news1.save()
        news2.save()
        news3.save()

        response = self.client.get(reverse("news:news"))

        self.assertIs(200, response.status_code)
        self.assertQuerysetEqual([news3, news2, news1], response.context["news"])

    def test_page_details(self):
        page = News(title="Привет!",
                    content="Ты выиграл грант на курс!",
                    created_at=timezone.now() + timedelta(hours=1)
                    )
        page.save()

        response = self.client.get(reverse("news:get_page", args=(page.id,)))

        self.assertIs(200, response.status_code)
        self.assertQuerysetEqual("Привет!", response.context["news"].title)
        self.assertQuerysetEqual("Ты выиграл грант на курс!", response.context["news"].content)
        self.assertEqual(page.created_at, response.context["news"].created_at)

    def test_page_order_comments(self):
        page = News(title="Гоооол!",
                    content="Казахстан выиграл в футболе против Дании!",
                    created_at=timezone.now() + timedelta(hours=1)
                    )
        comment1 = Comments(content="Ура!", created_at=timezone.now() + timedelta(hours=1), News=page)
        comment2 = Comments(content="Молодцы!", created_at=timezone.now() + timedelta(hours=2), News=page)
        comment3 = Comments(content="Отскок!", created_at=timezone.now() + timedelta(hours=3), News=page)

        page.save()
        comment1.save()
        comment2.save()
        comment3.save()

        response = self.client.get(reverse("news:get_page", args=(page.id,)))

        self.assertQuerysetEqual([comment3, comment2, comment1], response.context["comments"])
