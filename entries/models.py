from django.db import models
from users.models import User


class Entry(models.Model):
    entry_title = models.CharField(max_length=255)
    entry_text = models.TextField()
    entry_slug = models.SlugField(unique=True, null=True, blank=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "entries"
        ordering = ["-entry_date"]

    def __str__(self):
        return self.entry_title
