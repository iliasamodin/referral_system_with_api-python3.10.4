from django.db import models


class APIPath(models.Model):
    path = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.path


# Model of accepted keys for api addresses
class Key(models.Model):
    GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS, TRACE = \
        "get", "post", "put", "patch", "delete", "head", "options", "trace"
    REQUEST_OPTIONS = [
        (GET, "get"),
        (POST, "post"),
        (PUT, "put"),
        (PATCH, "patch"),
        (DELETE, "delete"),
        (HEAD, "head"),
        (OPTIONS, "options"),
        (TRACE, "trace")
    ]

    api_path = models.ForeignKey(APIPath, null=False, on_delete=models.CASCADE)
    key = models.CharField(max_length=50, default="", blank=True)
    request_type = models.CharField(
        max_length=7,
        choices=REQUEST_OPTIONS,
        default=GET
    )
    description = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["api_path", "id"]

    def __str__(self):
        return f"{self.key} for {self.api_path.path}"