from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from twitter_clone.forms import CreateUserForm, PostForm, AuthenticateForm
from twitter_clone.models import Post, User


def index(request, post_form=None):
    user = request.user
    if user.is_authenticated():
        post_form = PostForm()
        feed = Post.objects.order_by('-date')[:10] 
        return render(request, 'twitter_clone/index.html', {'post_form': post_form, 'feed': feed, })
    else:
        auth_form = AuthenticateForm()
        user_form = CreateUserForm()
        return render(request, 'twitter_clone/login.html', {'auth_form': auth_form, 'user_form': user_form, })
    

def create_user(request):
    form = CreateUserForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.clean_email()
            password = form.clean_password2()
            f = form.save()
            user = authenticate(email = email, password = password)
            login(request, user)
            return redirect('feed:index')
        else:
            return redirect('feed:server_error') 
    return redirect('feed:index')
 
 
def login_user(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('feed:index')
        else:
            return redirect('feed:not_found')
    else:  
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
        return redirect('feed:single_post', post.id )
    else:
        return login(request)
          
    return redirect('feed:index')
  
  
@login_required 
def edit(request, post_id):
    old = get_object_or_404(Post, pk=post_id)
    if old.is_editable():
        if old.poster != request.user:
            return HttpResponseForbidden()
        else:
            post = Post(poster=request.user)

        if request.method == 'POST':
            new = PostForm(data=request.POST, instance=post)
            if new.is_valid():
                post = new.save(commit=False)
                old.text = post.text
                old.save()
                return redirect('feed:single_post', old.id )
        else:
            post = PostForm(instance=post)
    
        return redirect('feed:single_post', old.id )
    else:
        return HttpResponseForbidden()


@login_required
def single_post(request, post_id):
    post_form = PostForm()
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'twitter_clone/single_post.html', {'post': post, 'post_form': post_form, })

    
@login_required
def profile(request, user_id):
    user_p = get_object_or_404(User, pk=user_id)
    return render(request, 'twitter_clone/single_user.html', {'user_p': user_p, })


@login_required    
def follow(request):
    if request.method == 'POST':
        follow_user = request.POST.get('follow', False)
        if follow_user:
            try:
                follow = User.objects.get(id=follow_user)
                req = request.user
                from twitter_clone.models import RELATIONSHIP_FOLLOWING
                req.add_relationship(follow, RELATIONSHIP_FOLLOWING)
            except ObjectDoesNotExist:
                raise Http404
        return redirect('feed:profile', follow.id )
 
        
def not_found(request):
    return render(request, 'twitter_clone/404.html')
    

def server_error(request):
    return render(request, 'twitter_clone/500.html')