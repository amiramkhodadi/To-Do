from django.conf import settings
from django.db import models


class TODOO(models.Model):
    srno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title
