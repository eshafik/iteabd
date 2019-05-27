from django import template
from django.db.models import Count

from blog.models import Post


register = template.Library()

#showing total blog post
@register.simple_tag
def total_posts():
    return Post.objects.published_posts().count()


#showing all latest post from render template
@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.published_posts().exclude(category='notice').order_by('-publish')[:5]

    return {'latest_posts':latest_posts}

#showing latest post for members
@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts_for_member(count=5):
    latest_posts = Post.objects.published_posts().filter(show_to__in=['member', 'public'], status=True).exclude(category='notice').order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing latest post for public
@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts_for_public(count=5):
    latest_posts = Post.objects.published_posts().filter(show_to='public', status=True).exclude(category='notice').order_by('-publish')[:count]

    return {'latest_posts':latest_posts}


#showing most commented posts
@register.simple_tag
def get_most_commented_posts(count=5):

    return Post.objects.published_posts().annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

#showing yarn catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def yarn_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='yarn', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}   

#showing Fabric catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def fabric_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='fabric', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing wet catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def wet_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='wet', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing apparel catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def apparel_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='apparel', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing Printing catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def printing_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='printing', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing merchandizing catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def merchandising_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='merchandising', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing others catergory posts
@register.inclusion_tag('blog/latest_posts.html')
def others_category(count=5):
    latest_posts = Post.objects.published_posts().filter(category='others', status=True).order_by('-publish')[:count]

    return {'latest_posts':latest_posts}

#showing notice catergory posts for executive
@register.inclusion_tag('blog/latest_posts.html')
def notice_category_executive(count=5):
    latest_posts = Post.objects.published_posts().filter(category='notice', status=True).order_by('-publish')[:count]
    
    return {'latest_posts':latest_posts}

#showing notice catergory posts for members
@register.inclusion_tag('blog/latest_posts.html')
def notice_category_member(count=5):
    latest_posts = Post.objects.published_posts().filter(category='notice', status=True, show_to__in=['member', 'public']).order_by('-publish')[:count]
    
    return {'latest_posts':latest_posts}