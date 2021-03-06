from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *
from .email import *
import datetime as dt

# Create your views here.
# @login_required(login_url='/accounts/login/')
# def welcome(request):
#     profiles= Profile.objects.all()
#     current_user = request.user
#     return render(request,'welcome.html',{"profiles":profiles,"current_user":current_user})

@login_required(login_url='/accounts/login/')
def welcome(request):
    if request.user.is_authenticated:
        if Join.objects.filter(user_id=request.user).exists():
            hood = Neighborhood.objects.get(pk=request.user.join.hood_id.id)
            posts = Post.objects.filter(post_hood=request.user.join.hood_id.id)
            businesses = Business.objects.filter(
                biz_hood=request.user.join.hood_id.id)
            return render(request, 'current_hood.html', {"hood": hood, "businesses": businesses, "posts": posts})
        else:
            hoods = Neighborhood.all_neighborhoods()
            return render(request, 'welcome.html', {"hoods": hoods})
    else:
        hoods = Neighborhood.all_neighborhoods()
        return render(request, 'welcome.html', {"hoods": hoods})

@login_required(login_url='/accounts/login/')
def profile(request,id):
    user_object = request.user
    current_user = Profile.objects.get(username__id=request.user.id)
    user = Profile.objects.get(username__id=id)
    return render(request, "profile.html", {"current_user":current_user,"user":user,"user_object":user_object})

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user=request.user
    user_edit = Profile.objects.get(username__id=current_user.id)
    if request.method =='POST':
        form=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()

        return redirect("welcome")               
    else:
        form=ProfileForm(instance=request.user.profile)
     
    return render(request,'edit_profile.html',locals())

@login_required(login_url='/accounts/login/')
def user_profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_info = Profile.get_profile(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)
    businesses = Business.get_profile_businesses(profile.id)
    title = f'@{profile.username}'
    return render(request, 'profile.html', {'title': title, 'profile': profile, 'profile_info': profile_info, 'businesses': businesses})


@login_required(login_url='/accounts/login/')
def new_hood(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user_profile = current_user
            hood.save()
        return redirect('welcome')

    else:
        form = AddHoodForm()
    return render(request, 'add_hood.html', {"form": form})

@login_required(login_url='/accounts/login/')
def join_hood(request, hood_id):
    '''
    This view function will implement adding 
    '''
    neighborhood = Neighborhood.objects.get(pk=hood_id)
    if Join.objects.filter(user_id=request.user).exists():

        Join.objects.filter(user_id=request.user).update(hood_id=neighborhood)
    else:

        Join(user_id=request.user, hood_id=neighborhood).save()

    return redirect('welcome')

@login_required(login_url='/accounts/login/')
def leave_hood(request, hood_id):
    '''
    This function will delete a neighbourhood instance in the join table
    '''
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.get(user_id=request.user).delete()
        return redirect('welcome')


@login_required(login_url='/accounts/login/')
def new_biz(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddBizForm(request.POST, request.FILES)
        if form.is_valid():
            biz = form.save(commit=False)
            biz.biz_owner = current_user
            biz.biz_hood = request.user.join.hood_id
            biz.save()
        return redirect('welcome')

    else:
        form = AddBizForm()
    return render(request, 'add_biz.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.poster = current_user
            post.post_hood = request.user.join.hood_id
            post.save()
        return redirect('welcome')

    else:
        form = AddPostForm()
    return render(request, 'add_post.html', {"form": form})


def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        business_results = Business.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "businesses": business_results})

    else:
        message = "Please enter a search term"
        return render(request, 'search.html', {"message": message})
