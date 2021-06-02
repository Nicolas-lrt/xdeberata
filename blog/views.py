from django.shortcuts import render, redirect
from .forms import CommentForm, CommentLoggedForm

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


def add_comment_logged(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        name = request.username
        email = request.email
        content = request.POST.get('content')



def postList(request):
    posts = Post.objects.all()

    return render(request, 'blog/post-list.html', {'posts': posts})
