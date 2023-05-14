from datetime import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views import View

from .filters import PostFilter
from .models import Post, Comment
from django.contrib import messages
from .forms import CustomUserCreationForm, PostForm, CommentForm, UpdateUserForm, UserForms


def index(request):
    return render(request, "base.html")


# -------------------------------------

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid data')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts')
        else:
            messages.error(request, 'username or password incorrect')
    context = {}
    return render(request, 'logIn.html', context)


def register(request):
    user = CustomUserCreationForm()
    if request.method == 'POST':
        user = CustomUserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            messages.success(request, "Registration sucessful")
            return redirect('login')
        else:
            messages.error(request, user.errors)
    context = {'user': user}
    return render(request, 'register.html', context)


def get_post(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'Joo/post_list.html', context)


def get_post_history(request):
    posts = Post.objects.all()
    recently_viewed_posts = Post.objects.all().order_by('-last_visit')[0:4]
    context = {
        'posts': posts,
        'recently_viewed_posts': recently_viewed_posts
               }
    return render(request, 'Joo/history.html', context)

def get_post_able(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'Joo/post-able.html', context)


def post_detail(request, id):
    posts = Post.objects.filter(id=id)
    post = get_object_or_404(Post, id=id)
    post.num_visits = post.num_visits + 1
    post.last_visit = datetime.now()
    post.save()
    context = {'posts': posts}
    return render(request, 'Joo/post_deatil.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_superuser:
                form.save()
                return redirect('posts')
            else:
                item = form.save(commit=False)
                item.in_active = False
                #item.creator_id = (User.objects.get(request.user.username))
                item.save()
                return redirect('posts')
    context = {'form': form}
    return render(request, 'Joo/post_form.html', context)


@login_required(login_url='login')
def update_post(request, id):
    if request.user.is_superuser:
        post = Post.objects.get(id=id)
        form = PostForm(instance=post)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts')
        context = {'form': form}
        return render(request, 'Joo/post_update.html', context)
    else:
        messages.error(request, 'you doesnt have root')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def delete_post(request, id):
    if request.user.is_superuser:
        post = Post.objects.get(id=id)
        if request.method == 'POST':
            post.delete()
            return redirect('posts')
        context = {'post': post}
        return render(request, 'Joo/post-delete.html', context)
    else:
        messages.error(request, 'you doesnt have root')


# def comment(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    comment = post.comment_set.all()
#    context = {'comment': comment}
#    return render(request, "Joo/comment.html", context)

def comment(request):
    comment = Comment.objects.all()
    context = {'comment': comment}
    return render(request, 'Joo/comment.html', context)


def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comment_set.all()
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('posts')
    else:
        comment_form = CommentForm()
    context = {'form': new_comment}
    return render(request, 'Joo/comment-create.html', context)


def editProfile(request, id):
    user = User.objects.get(id=id)
    form = UpdateUserForm(instance=user)
    if request.user.is_active:
        if request.method == 'POST':
            form = UpdateUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('posts')
    context = {'form': form}
    return render(request, 'Joo/profile-edit.html', context)


class PasswordsChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'Joo/password-change.html'
    success_url = reverse_lazy('success-password')


def password_success(request):
    return render(request, 'Joo/password-success.html')


def get_users(request):
    User = get_user_model()
    users = User.objects.values()
    form = UserForms()
    context = {'users': users, 'form': form}
    return render(request, 'Joo/edit-users.html', context)


def update_users(request, id):
    users = User.objects.get(id=id)
    form = UserForms(instance=users)
    if request.method == 'POST':
        form = UserForms(request.POST, instance=users)
        if form.is_valid():
            form.save()
            return redirect('users')
    context = {'form': form}
    return render(request, 'Joo/update-users.html', context)


def delete_users(request, id):
    users = User.objects.get(id=id)
    if request.method == 'POST':
        users.delete()
        return redirect('users')
    context = {'users': users}
    return render(request, 'Joo/delete-users.html', context)


def add_users(request):
    user = CustomUserCreationForm()
    if request.method == 'POST':
        user = CustomUserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('users')
        else:
            messages.error(request, user.errors)
    context = {'user': user}
    return render(request, 'Joo/add_users.html', context)


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        post = Post.objects.filter(name__contains=search)
        context = {'search': search, 'posts': post}
        return render(request, 'Joo/post_list.html', context)


def search_date(request):
    if request.method == 'POST':
        publication_date = request.POST['publication_date']
        post = Post.objects.filter(publication_date=publication_date)
        context = {'posts': post}
        return render(request, 'Joo/post_list.html', context)


def search_num_visits(request):
    if request.method == 'POST':
        search_num = request.POST['search-num']
        post = Post.objects.filter(num_visits=search_num)
        context = {'posts': post}
        return render(request, 'Joo/post_list.html', context)



class CreatePostView(View):
    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'Joo/post_form.html', context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_superuser:
                form.save()
                return redirect('posts')
            else:
                item = form.save(commit=False)
                item.in_active = False
                # item.creator_id = (User.objects.get(request.user.username))
                item.save()
                return redirect('posts')
        context = {'form': form}
        return render(request, 'Joo/post_form.html', context)


class UpdatePostView(View):
    def get(self, request, id):
        if request.user.is_superuser:
            post = Post.objects.get(id=id)
            form = PostForm(instance=post)
            context = {'form': form}
            return render(request, 'Joo/post_update.html', context)
        else:
            messages.error(request, 'you dont have root')
            return redirect('posts')

    def post(self, request, id):
        if request.user.is_superuser:
            post = Post.objects.get(id=id)
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts')
            context = {'form': form}
            return render(request, 'Joo/post_update.html', context)
        else:
            messages.error(request, 'you dont have root')
            return redirect('posts')


class DeletePostView(View):
    def get(self, request, id):
        if request.user.is_superuser:
            post = Post.objects.get(id=id)
            context = {'post': post}
            return render(request, 'Joo/post-delete.html', context)
        else:
            messages.error(request, 'you dont have root')
            return redirect('posts')

    def post(self, request, id):
        if request.user.is_superuser:
            post = Post.objects.get(id=id)
            post.delete()
            return redirect('posts')
        else:
            messages.error(request, 'you dont have root')
            return redirect('posts')