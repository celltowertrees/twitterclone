from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from twitter_clone.forms import CreateUserForm, PostForm, AuthenticateForm
from twitter_clone.models import Post, User


def index(request, post_form=None):
    user = request.user
    if user.is_authenticated():
        post_form = PostForm()
        feed = Post.objects.order_by('date')[:10]  
        return render(request, 'twitter_clone/index.html', {'post_form': post_form, 'feed': feed, })
    else:
        auth_form = AuthenticateForm()
        user_form = CreateUserForm()
        return render(request, 'twitter_clone/login.html', {'auth_form': auth_form, 'user_form': user_form, })


def create_user(request):
    form = CreateUserForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password2()
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('feed:profile', {'username': username})
        else:
            return index(request, user_form=user_form)
    return redirect('feed:index')
 
 
def login_user(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('feed:index')
        else:
            return index(request, auth_form=form)
        return redirect('feed:index')
        

def logout_user(request):
    logout(request)
    return redirect('feed:index')
    

@login_required
def submit(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster = request.user
            post.save()
        return render(request, 'twitter_clone/single_post.html', {'post': post, })
    else:
        return login(request)
          
    return redirect('feed:index')


@login_required
def single_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'twitter_clone/single_post.html', {'post': post})

    
@login_required
def profile(request, user_id):
    post_user = get_object_or_404(User, pk=user_id)
    return render(request, 'twitter_clone/single_user.html', {'post_user': post_user})
    

@login_required 
def edit(request, post_id):
    return HttpResponse("You are editing Post %s." % post_id)
