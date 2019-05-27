from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from .query_set import PostQuerySet

# Create your models here.


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published_posts(self):
        return self.get_queryset().published_posts()
    
    def search(self,query):
        return self.get_queryset().search(query)



class Post(models.Model):
    POST_STATUS_CHOICES=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    SHOW_CHOICES = (
        ('public', 'Public'),
        ('member', 'Member'),
        ('executive', 'Executive'),
    )
    POST_CATAGORY=(
        ('yarn', 'Yarn'),
        ('fabric', 'Fabric'),
        ('wet', 'Wet Processing'),
        ('apparel', 'Apparel'),
        ('printing', 'Printing'),
        ('merchandising', 'Merchandising'),
        ('notice', 'Notice'),
        ('others', 'Others'),

    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    title = models.CharField(max_length=250)
    # slug = models.SlugField(max_length=250, unique_for_date='publish',
    #                         allow_unicode=True)
    tags = TaggableManager()
    photo = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True,null=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post_status = models.CharField(max_length=10,
                                   choices=POST_STATUS_CHOICES,
                                   default='draft')
    show_to = models.CharField(max_length=10,
                               choices=SHOW_CHOICES,
                               default='member')
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=POST_CATAGORY,
                                default='others')

    objects = PostManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #             args=[self.publish.year,
    #             self.publish.month,
    #             self.publish.day,
    #             self.id])
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                args=[self.id])

    # def save(self, *args, **kwargs):
    #     print(type(self.title))
    #     self.slug = slugify(self.title,allow_unicode=True)
    #     print(self.slug)
    #     print(type(self.slug))
    #     super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='replies')

    class Meta:
        # sort comments in chronological order by default
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {}'.format(self.post.author)