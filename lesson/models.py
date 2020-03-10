from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='public', publish__year='2020')


class Material(models.Model):
    MATERIAL_TYPES = (
        ('theory', 'Theoretical'),
        ('practice', 'Practical'),
    )

    STATUS_TYPES = (
        ('private', 'Draft'),
        ('public', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    material_type = models.CharField(max_length=20,
                                     choices=MATERIAL_TYPES,
                                     default='theory')
    status = models.CharField(max_length=20,
                              choices=STATUS_TYPES,
                              default='private')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_materials')
    objects = models.Manager()
    published = PublishedManager()
#     class Meta:
#         ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson:material_details',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])


class Comment(models.Model):
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return "Profile for {}".format(self.user.username)
