from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, likePost, followersCount
from itertools import chain
import random

# initiliaze the web server: python manage.py runserver
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = followersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # posts = Post.objects.all()
    # user suggestions
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list)) 

    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This e-mail is already registered!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This username is already registered!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Login and redirect to settings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Create a user profile
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user.id)
                new_profile.save()
                return redirect('settings')
            
        else:
            messages.info(request, 'Password does not match!')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Incorrect username or password!')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method =='POST': 
        if request.FILES.get('photo') == None:
            photo = user_profile.profile_photo
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_photo = photo
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        elif request.FILES.get('photo') != None:
            photo=request.FILES.get('photo')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_photo = photo
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        photo = request.FILES.get('photo_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, photo=photo, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    filter_likes = likePost.objects.filter(post_id=post_id, username=username).first()
    if filter_likes == None:
        new_like = likePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.nr_of_likes = post.nr_of_likes + 1
        post.save()
        return redirect('/')
    else: 
        filter_likes.delete()
        post.nr_of_likes = post.nr_of_likes - 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if followersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(followersCount.objects.filter(user=pk))
    user_following = len(followersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if followersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = followersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = followersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)

    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    if request.method =='POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html',{'user_profile': user_profile, 'username_profile_list': username_profile_list})