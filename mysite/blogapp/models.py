from django.db import models
from django.urls import reverse



class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("article", kwargs={"pk": self.pk})
