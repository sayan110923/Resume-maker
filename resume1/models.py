from django.db import models

# Create your models here.
from django.db import models


class profile(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    about = models.TextField()
    collage = models.CharField(max_length=200)
    degree = models.CharField(max_length=20)
    project1 = models.TextField()

class resumeProfile(models.Model):

    resume_id = models.ForeignKey(profile, on_delete=models.CASCADE)