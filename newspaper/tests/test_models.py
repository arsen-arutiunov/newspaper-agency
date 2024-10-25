from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Newspaper, Topic


class ModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create(username="test",
                                                   first_name="test",
                                                   last_name="test")
        self.assertEqual(str(redactor), redactor.username)

    def test_newspaper_str(self):
        newspaper = Newspaper.objects.create(title="test",
                                             content="test")

        newspaper.publishers.set([])
        topic = Topic.objects.create(name="test")
        newspaper.topics.add(topic)

        self.assertEqual(str(newspaper), newspaper.title)

    def test_create_redactor_with_years_of_experience(self):
        username = "test"
        first_name = "test"
        last_name = "test"
        years_of_experience = 5
        password = "<PASSWORD>"

        redactor = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            years_of_experience=years_of_experience,
            password=password)

        self.assertEqual(redactor.username, username)
        self.assertEqual(redactor.first_name, first_name)
        self.assertEqual(redactor.last_name, last_name)
        self.assertEqual(redactor.years_of_experience, years_of_experience)
        self.assertTrue(redactor.check_password(password))

    def test_get_absolute_url_in_redactor(self):
        redactor = get_user_model().objects.create_user(username="test",
                                                        first_name="test",
                                                        last_name="test")
        self.assertEqual(redactor.get_absolute_url(),
                         reverse("newspaper:redactor-detail",
                                 kwargs={"pk": redactor.pk}))
