from django.urls import reverse

from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="redactor",
            password="<PASSWORD>",
            years_of_experience=5
        )

    def test_years_of_experience_listed(self):
        """
        Test redactor's experience is in list_display on redactor admin page.
        """
        url = reverse("admin:newspaper_redactor_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_detail_years_of_experience_listed(self):
        """
        Test redactor's experience is on redactor detail admin page.
        """
        url = reverse("admin:newspaper_redactor_change",
                      args=[self.redactor.pk])
        res = self.client.get(url)
        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_detail_added_fieldsets_listed(self):
        """
        Test redactor's experience,
        first name and last name are on
        redactor detail admin page.
        """
        url = reverse("admin:newspaper_redactor_change",
                      args=[self.redactor.pk])
        res = self.client.get(url)
        self.assertContains(res, self.redactor.years_of_experience)
        self.assertContains(res, self.redactor.first_name)
        self.assertContains(res, self.redactor.last_name)
