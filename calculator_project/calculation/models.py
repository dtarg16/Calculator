from django.db import models
from django.contrib.auth.models import User


class Calculation(models.Model):
    expression = models.CharField(max_length=255)
    result = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expression} = {self.result}"
