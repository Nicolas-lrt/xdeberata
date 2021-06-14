from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from slugify import slugify

from account.decorators import admin_only
from account.models import Account
from .forms import CommentForm, CommentLoggedForm, AddPost

# Create your views here.
from blog.models import Post, Comments


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def miniindex(request):
    return render(request, 'home-minimal.html')


def error404page(request):
    return render(request, '404-error.html')


def aboutPage(request):
    return render(request, 'about.html')


def postPage(request, slug):
    post = Post.objects.get(slug=slug)
    logged = request.user.is_authenticated
    admin = 0
    for group in request.user.groups.all():
        if group.name == 'admin':
            admin = 1
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

    return render(request, 'blog/post.html', {'post': post, 'form': form, 'admin': admin})


def postList(request):
    posts = Post.objects.all()
    admin = 0
    for group in request.user.groups.all():
        if group.name == 'admin':
            admin = 1
    return render(request, 'blog/post-list.html', {'posts': posts, 'admin': admin})


@admin_only
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('post-list')


@admin_only
def delete_comment(request, pk):
    comment = Comments.objects.get(id=pk)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@admin_only
def add_post(request):
    author = Account.objects.get(user_id=request.user.id)
    form = AddPost()
    if request.method == 'POST':
        form = AddPost(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            slug = slugify(title)
            post = Post(author_id=author.id,
                        title=title,
                        body=request.POST.get('body'),
                        bodyPreview=request.POST.get('bodyPreview'),
                        main_img=request.FILES["main_img"],
                        slug=slug)
            post.save()

            return redirect('post-list')

    return render(request, 'blog/add-post.html', {'form': form})


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/update-post.html'
    fields = ['title', 'main_img', 'bodyPreview', 'body']
