from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Post,Profile,Comment,Like,Follow,User
# from .forms import NewPostForm,ProfileForm,CommentForm,LikeForm,FollowForm
# from django.db.models import Q
# import datetime as dt

# Create your views here.
@login_required(login_url='/accounts/login/')
def welcome(request):
    
    return render(request,'welcome.html')
