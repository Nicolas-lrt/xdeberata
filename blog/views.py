from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from slugify import slugify
from account.decorators import admin_only
from account.models import Account
from account.views import isAdmin
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
    post = Post.objects.get(slug_post=slug)
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

                return redirect('post_detail', slug=post.slug_post)
        else:
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()

                return redirect('post_detail', slug=post.slug_post)
    elif logged:
        form = CommentLoggedForm()
    else:
        form = CommentForm()

    return render(request, 'blog/post.html', {'post': post, 'form': form, 'admin': isAdmin(request)})


def postList(request):
    posts = Post.objects.all()
    return render(request, 'blog/post-list.html', {'posts': posts, 'admin': isAdmin(request)})


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
                        slug_post=slug)
            post.save()

            return redirect('post-list')

    return render(request, 'blog/add-post.html', {'form': form})


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/update-post.html'
    fields = ['title', 'main_img', 'bodyPreview', 'body']


@admin_only
def user_list(request):
    users = Account.objects.all()
    context = {'users': users}
    return render(request, 'account/user-list.html', context)


@admin_only
def user_profile(request, pk):
    user = Account.objects.get(id=pk)
    admin = 0
    for group in user.user.groups.all():
        if group.name == 'admin':
            admin = 1
    context = {'user': user, 'admin': admin}

    return render(request, 'account/user-profile.html', context)


@admin_only
def add_admin(request, pk):
    user = Account.objects.get(id=pk)
    admin_group = Group.objects.get(name="admin")
    admin_group.user_set.add(user.user)
    return redirect(request.META.get('HTTP_REFERER'))


@admin_only
def remove_admin(request, pk):
    user = Account.objects.get(id=pk)
    admin_group = Group.objects.get(name="admin")
    admin_group.user_set.remove(user.user)
    return redirect(request.META.get('HTTP_REFERER'))
