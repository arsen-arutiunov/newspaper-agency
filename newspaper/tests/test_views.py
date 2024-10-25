from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Newspaper, Redactor, Topic

TOPIC_URL = reverse("newspaper:topic-list")
NEWSPAPER_URL = reverse("newspaper:newspaper-list")
REDACTOR_URL = reverse("newspaper:redactor-list")


class PublicViewsTest(TestCase):
    def test_login_required(self):
        for url in [TOPIC_URL, NEWSPAPER_URL, REDACTOR_URL]:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_topics(self):
        Topic.objects.create(name="Box")
        Topic.objects.create(name="Football")
        response = self.client.get(TOPIC_URL)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(list(response.context["topic_list"]),
                         list(topics))
        self.assertTemplateUsed(response,
                                "newspaper/topic_list.html")

    def test_create_topic(self):
        form_data = {
            "name": "test",
        }
        self.client.post(reverse("newspaper:topic-create"), form_data)
        topic = Topic.objects.get(name="test")
        self.assertEqual(topic.name, form_data["name"])

    def test_retrieve_redactors(self):
        Redactor.objects.create(username="test1",
                                password="<PASSWORD>",
                                years_of_experience=5)
        Redactor.objects.create(username="test2",
                                password="<PASSWORD>",
                                years_of_experience=6)
        response = self.client.get(REDACTOR_URL)
        self.assertEqual(response.status_code, 200)
        redactors = Redactor.objects.all()
        self.assertEqual(list(response.context["redactor_list"]),
                         list(redactors))
        self.assertTemplateUsed(response,
                                "newspaper/redactor_list.html")

    def test_create_redactor(self):
        form_data = {
            "username": "test1",
            "password1": "1A2g3s4f1234",
            "password2": "1A2g3s4f1234",
            "first_name": "test",
            "last_name": "test",
            "years_of_experience": 5,
        }
        self.client.post(reverse("newspaper:redactor-create"), form_data)
        redactor = get_user_model().objects.get(
            username=form_data["username"])
        self.assertEqual(redactor.first_name, form_data["first_name"])
        self.assertEqual(redactor.last_name, form_data["last_name"])
        self.assertEqual(redactor.years_of_experience,
                         form_data["years_of_experience"])

    def test_retrieve_newspapers(self):
        newspaper = Newspaper.objects.create(title="test",
                                             content="test")

        newspaper.publishers.set([])
        topic = Topic.objects.create(name="test")
        newspaper.topics.add(topic)
        newspaper1 = Newspaper.objects.create(title="test1",
                                              content="test1")

        newspaper1.publishers.set([])
        topic = Topic.objects.create(name="test1")
        newspaper1.topics.add(topic)
        response = self.client.get(NEWSPAPER_URL)
        self.assertEqual(response.status_code, 200)
        newspapers = Newspaper.objects.all()
        self.assertEqual(list(response.context["newspaper_list"]),
                         list(newspapers))
        self.assertTemplateUsed(response,
                                "newspaper/newspaper_list.html")

    def test_create_newspaper(self):
        topic = Topic.objects.create(name="Technology")
        redactor = Redactor.objects.create(
            username="editor1",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )

        form_data = {
            "title": "Tech Daily",
            "content": "Latest tech news",
            "topics": [topic.id],
            "publishers": [redactor.id],
        }

        self.client.post(reverse("newspaper:newspaper-create"), form_data)

        self.assertEqual(Newspaper.objects.count(), 1)
        newspaper = Newspaper.objects.get(title="Tech Daily")
        self.assertEqual(newspaper.title, form_data["title"])
        self.assertEqual(newspaper.content, form_data["content"])
        self.assertIn(topic, newspaper.topics.all())
        self.assertIn(redactor, newspaper.publishers.all())


class RedactorSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.redactor1 = Redactor.objects.create(username="john_doe",
                                                 years_of_experience=1)
        self.redactor2 = Redactor.objects.create(username="jane_doe",
                                                 years_of_experience=2)
        self.redactor3 = Redactor.objects.create(username="doe_john",
                                                 years_of_experience=3)

    def test_search_form_no_results(self):
        response = self.client.get(REDACTOR_URL, {"username": "not_found"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["redactor_list"], [])

    def test_search_form_partial_match(self):
        response = self.client.get(REDACTOR_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 2)
        self.assertIn(self.redactor1, response.context["redactor_list"])
        self.assertIn(self.redactor3, response.context["redactor_list"])

    def test_search_form_full_match(self):
        response = self.client.get(REDACTOR_URL, {"username": "jane_doe"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 1)
        self.assertIn(self.redactor2, response.context["redactor_list"])

    def test_filtered_search_results_by_redactor(self):
        response = self.client.get(REDACTOR_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 2)
        self.assertEqual(list(response.context["redactor_list"]),
                         list(Redactor.objects.filter(
                             username__contains="john").order_by("id")))


class TopicSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.topic1 = Topic.objects.create(
            name="Monster")
        self.topic2 = Topic.objects.create(
            name="Technology")
        self.topic3 = Topic.objects.create(
            name="Mountain")

    def test_search_form_no_results(self):
        response = self.client.get(TOPIC_URL, {"name": "People"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["topic_list"], [])

    def test_search_form_partial_match(self):
        response = self.client.get(TOPIC_URL, {"name": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 2)
        self.assertIn(self.topic1, response.context["topic_list"])
        self.assertIn(self.topic3, response.context["topic_list"])

    def test_search_form_full_match(self):
        response = self.client.get(TOPIC_URL, {"name": "Technology"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 1)
        self.assertIn(self.topic2, response.context["topic_list"])

    def test_filtered_search_results_by_id(self):
        response = self.client.get(TOPIC_URL, {"name": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 2)
        self.assertEqual(list(response.context["topic_list"]),
                         list(Topic.objects.filter(
                             name__contains="M").order_by("pk")))


class NewspaperSearchFormTest(TestCase):
    def setUp(self):
        topic1 = Topic.objects.create(name="Technology")
        redactor1 = Redactor.objects.create(
            username="editor1",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )
        topic2 = Topic.objects.create(name="Animal")
        redactor2 = Redactor.objects.create(
            username="editor2",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )
        topic3 = Topic.objects.create(name="People")
        redactor3 = Redactor.objects.create(
            username="editor3",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.newspaper1 = Newspaper.objects.create(
            title="Mountain",
            content="Mountain",
        )
        self.newspaper1.publishers.set([redactor1.id])
        self.newspaper1.topics.add(topic1)

        self.newspaper2 = Newspaper.objects.create(
            title="Find",
            content="Find",
        )
        self.newspaper2.publishers.set([redactor2.id])
        self.newspaper2.topics.add(topic2)

        self.newspaper3 = Newspaper.objects.create(
            title="Maker",
            content="Maker",
        )
        self.newspaper3.publishers.set([redactor3.id])
        self.newspaper3.topics.add(topic3)

    def test_search_form_no_results(self):
        response = self.client.get(NEWSPAPER_URL, {"title": "Animal"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["newspaper_list"], [])

    def test_search_form_partial_match(self):
        response = self.client.get(NEWSPAPER_URL, {"title": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 2)
        self.assertIn(self.newspaper1, response.context["newspaper_list"])
        self.assertIn(self.newspaper3, response.context["newspaper_list"])

    def test_search_form_full_match(self):
        response = self.client.get(NEWSPAPER_URL, {"title": "Find"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)
        self.assertIn(self.newspaper2, response.context["newspaper_list"])

    def test_filtered_search_results_by_car(self):
        response = self.client.get(NEWSPAPER_URL, {"title": "M"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 2)
        self.assertEqual(list(response.context["newspaper_list"]),
                         list(Newspaper.objects.filter(
                             title__contains="M").order_by("id")))
