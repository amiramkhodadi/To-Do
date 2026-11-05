from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TODOO(models.Model):
    srno = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(
        default=False,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
