from django.shortcuts import render, redirect

from account.decorators import admin_only
from account.models import Account
from .forms import CommentForm, CommentLoggedForm, AddPost

# Create your views here.
from blog.models import Post


def index(request):
    return render(request, 'index.html')


def miniindex(request):
    return render(request, 'home-minimal.html')


def error404page(request):
    return render(request, '404-error.html')


def aboutPage(request):
    return render(request, 'about.html')


def postPage(request, slug):
    post = Post.objects.get(slug=slug)
    logged = request.user.is_authenticated
    if request.method == 'POST':
        if logged:
            form = CommentLoggedForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.name = request.user.username
                comment.email = request.user.email
                comment.save()

                return redirect('post_detail', slug=post.slug)
        else:
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()

                return redirect('post_detail', slug=post.slug)
    elif logged:
        form = CommentLoggedForm()
    else:
        form = CommentForm()

    return render(request, 'blog/post.html', {'post': post, 'form': form})


def postList(request):
    posts = Post.objects.all()

    return render(request, 'blog/post-list.html', {'posts': posts})


@admin_only
def add_post(request):
    author = Account.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = AddPost(request.POST)
        if form.is_valid():
            post = Post(author_id=author.id,
                        title=request.POST.get('title'),
                        body=request.POST.get('body'),
                        main_img=request.POST.get('main_img'))
            post.save()

            return redirect('post-list')
    else:
        form = AddPost()
    return render(request, 'blog/add-post.html', {'form': form})
