from mysite.models import Topic,User,Forum,Post
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.paginator import Paginator
from .forms import TopicForm, PostForm
from mysite.settings import *

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def forum(request):
    """Listing of topics in a forum."""
    topics = Topic.objects.all()
    topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)
    userList = User.objects.values()

    if not Forum.objects.all():
        forum = Forum(title="HS Forum", description = "Let's talk !" , creator = request.user)
        forum.save()

    return render(request, 'django_simple_forum/forum.html', {'topics': topics, 'user': request.user, 'pk': 1, 'userList': userList})

def topic(request, topic_id):
    """Listing of posts in a topic."""
    posts = Post.objects.filter(topic=topic_id).order_by("created")
    posts = mk_paginator(request, posts, DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE)
    topic = Topic.objects.get(pk=topic_id)
    userList = User.objects.values()

    return render(request, 'django_simple_forum/topic.html', {'posts': posts, 'user': request.user, 'pk': topic_id, 'topic':topic, 'userList': userList})

def post_reply(request, topic_id):
    form = PostForm()
    topic = Topic.objects.get(pk=topic_id)
    userList = User.objects.values()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.creator = request.user

            post.save()

            return redirect('forum-detail')

    return render(request, 'django_simple_forum/reply.html', {'form': form, 'user': request.user, 'topic': topic, 'userList': userList})


def new_topic(request, forum_id):
    form = TopicForm()
    forum = Forum.objects.get(pk=forum_id)
    userList = User.objects.values()

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.forum = forum
            topic.creator = request.user
            topic.save()
            return redirect('forum-detail')

    return render(request, 'django_simple_forum/new-topic.html', {'form': form, 'user': request.user, 'userList': userList})