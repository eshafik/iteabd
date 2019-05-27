from itertools import chain

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User





class PostQuerySet(models.QuerySet):
    def published_posts(self):
        return self.filter(post_status='published', status=True)

    def search(self, query):
        post = self.filter(Q(title__contains=query)|Q(body__contains=query)|Q(tags__name__in=[query]))
        user = User.objects.filter(Q(first_name__contains=query)|Q(last_name__contains=query))
        results = chain(post, user)
        return results
        