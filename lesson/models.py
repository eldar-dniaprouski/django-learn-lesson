from django.db import models

# Create your models here.

class Material(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date=)
    body = models.TextField