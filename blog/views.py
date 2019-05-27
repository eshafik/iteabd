from django.shortcuts import render,redirect,get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 

from taggit.models import Tag

from .models import Post,Comment
from account.models import Profile
from .forms import PostForm, CommentForm, SearchForm


def home(request):
    return render(request,'home.html')

@login_required
def create_post(request):
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        post_form = None
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully.')
            return redirect(post_form)
        else:
             messages.error(request, 'Error creating your post.')
    else:
        post_form = PostForm()
    return render(request,'blog/create_post.html', {'post_form': post_form})

def post_list(request, tag_slug=None):
    object_list = Post.objects.published_posts()
    if not request.user.is_authenticated:
        object_list = Post.objects.published_posts().filter(show_to='public')
    else:
        if request.user.profile.itea_status=='executive':
            object_list = Post.objects.published_posts()
        elif request.user.profile.itea_status=='member':
            object_list = Post.objects.published_posts().filter(show_to__in=['member', 'public'])
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag, name=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html', {'posts': posts,'tag': tag})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    # For similiar post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.published_posts().filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    # For comment
    comments = post.comments.filter(active=True, parent__isnull=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    # create reply comment object
                    reply_comment = comment_form.save(commit=False)
                    # assign parent_obj to reply comment
                    reply_comment.parent = parent_obj
                    reply_comment.user = request.user

            # normal comment
            # create comment object but don't save to database
            new_comment = comment_form.save(commit=False)
            new_comment.post = post 
            new_comment.user = request.user
            new_comment.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    
    return render(request,'blog/post_detail.html', 
                  {'post':post, 'similar_posts': similar_posts,
                  'comments':comments,
                  'comment_form': comment_form})


@login_required
def post_edit(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method=='POST':
        form = PostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.save()
            form.save_m2m()
            messages.success(request, 'Post edited successfully.')
            return redirect(post_form)
        else:
             messages.error(request,'Error editing your post.')
    else:
        post_form = PostForm(instance=post)
    return render(request, 'blog/create_post.html', {'post_form': post_form})

@login_required
def post_delete(request,id):
    post = get_object_or_404(Post, id=id)
    post.status = False
    post.save()

    return redirect('blog:post_list')

def post_search(request):
    query = None
    results = None
    if request.method=='GET':
        query = request.GET.get('search_box')
        if query:
            results = Post.objects.search(query)
            

    return render(request, 'blog/search.html',{'query': query,'results': results})

@login_required
def draft_list(request):
    posts = request.user.blog_posts.filter(post_status='draft', status=True)

    return render(request, 'blog/draft_list.html', {'posts': posts})

@login_required
def my_published_post(request):
    posts = request.user.blog_posts.filter(post_status='published', status=True)

    return render(request, 'blog/draft_list.html', {'posts': posts})

def yarn(request):
    posts = Post.objects.filter(category='yarn', status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})

def fabric(request):
    posts = Post.objects.filter(category='fabric', status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})

def wet(request):
    posts = Post.objects.filter(category='wet', status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})

def apparel(request):
    posts = Post.objects.filter(category='apparel', status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})

def printing(request):
    posts = Post.objects.filter(category='printing',status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})

def merchandising(request):
    posts = Post.objects.filter(category='merchandising',status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})

def others(request):
    posts = Post.objects.filter(category='others', status=True).order_by('-publish')
    return render(request,'blog/draft_list.html', {'posts': posts})

@login_required
def notice(request):
    if request.user.profile.itea_status=='member':
        posts = Post.objects.filter(category='notice', show_to__in=['member', 'public'], status=True)
    else:
        posts = Post.objects.filter(category='notice', status=True)
    return render(request, 'blog/draft_list.html', {'posts': posts})



