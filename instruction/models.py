from django.db import models


class APIPath(models.Model):
    path = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.path