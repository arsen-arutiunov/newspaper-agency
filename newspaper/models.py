from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0,
                                                      blank=False,
                                                      null=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="redactor_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="redactor_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def get_absolute_url(self):
        return reverse("newspaper:redactor-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username


class Newspaper(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topics = models.ManyToManyField(Topic,
                                    blank=False,
                                    related_name="newspapers")
    publishers = models.ManyToManyField(Redactor,
                                        blank=False,
                                        related_name="newspapers")

    class Meta:
        verbose_name = "newspaper"
        verbose_name_plural = "newspapers"

    def short_content(self):
        return ".".join(self.content.split(".")[:4]) + "..."

    def __str__(self):
        return self.title
