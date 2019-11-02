from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile,User
# from .forms import NewPostForm,ProfileForm,CommentForm,LikeForm,FollowForm
# from django.db.models import Q
# import datetime as dt

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    profiles= Profile.objects.all()
    current_user = request.user
    return render(request,'welcome.html',{"profiles":profiles,"current_user":current_user})


@login_required(login_url='/accounts/login/')
def profile(request,id):
    user_object = request.user
    current_user = Profile.objects.get(username__id=request.user.id)
    user = Profile.objects.get(username__id=id)
    # posts = Post.objects.filter(upload_by = user)
    # posts = Post.objects.all()
    # follows = Follow.objects.all()
    return render(request, "profile.html", {"current_user":current_user,"user":user,"user_object":user_object})
