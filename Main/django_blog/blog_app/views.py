from django.shortcuts import render, redirect
from blog_app.forms import UserForm, UserProfileInfoForm, PostForm, UpdateUserForm
from blog_app.models import Post,UserProfileInfo
from django.views.generic import  DetailView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from blog_app.models import Post
from django.core.files.storage import FileSystemStorage
from django.db.models import Q


# Create your views here.

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog_app/article.html'
    

# class AddPostView(CreateView):
#     model =Post
#     # model1 = UserForm

#     # user1= UserForm.username

#     template_name = 'blog_app/addpost.html'
#     fields = ['title',  'content', 'status']

def addpost(request):

    if request.method == 'POST':
        post_form = PostForm(data=request.POST, files=request.FILES)

        if post_form.is_valid():
            blogpost = post_form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            return redirect( 'user_profile')
    
        # else:
        #     print(post_form.error)
    else:
        post_form = PostForm()

    return render (request, 'blog_app/addpost.html', {'post_form':post_form,})

#function to delete 
def deletepost(request,id):
    posts = Post.objects.get(id=id)
    if request.method == "POST":
        posts.delete()
        return redirect('user_profile')
    return render (request, 'blog_app/deletepost.html', {'post':posts})


#function to edit
def editpost(request, id):
    post = Post.objects.get(id=id)
    blog=PostForm(instance=post)
    if request.method=="POST":
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect( 'user_profile')
    return render(request, "blog_app/editpost.html", {'blog':post,})
#for search 
def searchpost(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = Post.objects.filter(Q(title__contains=searched) | Q(content__contains=searched))
        post_dict = {'post_list': blogs}

        return render(request, 'blog_app/user_profile.html', post_dict, {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "blog_app/user_profile.html", {})

#function to edit profile
def editprofile(request):
    user = request.user
    userpro =UpdateUserForm(instance=user)
    profile_form = UserProfileInfoForm(instance=request.user.userprofileinfo)

    if request.method=="POST":
        user_form = UpdateUserForm(data=request.POST, instance=request.user)
        profile_form = UserProfileInfoForm(request.POST, request.FILES, instance=request.user.userprofileinfo)

        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect( 'user_profile')
    return render(request, "blog_app/editprofile.html", {'user_form':userpro, 'profile_form': profile_form})


def index(request):
     return render(request, 'blog_app/index.html')


@login_required
def user_profile(request):
    queryset = Post.objects.filter(status=1)
    post_dict = {'post_list': queryset}
    return render(request, 'blog_app/user_profile.html', context=post_dict)



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']

            # profile.save()
            image = request.FILES['profile_pic']
            if image:
                filename = FileSystemStorage().save('profile_pics/' + image.name, image)
                profile.profile_pic = filename
            profile.save()
            
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'blog_app/registration.html', 
                  {'user_form':user_form,
                  'profile_form':profile_form,
                  'registered':registered
                  })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse(user_profile))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details!")

    else:
        return render(request, 'blog_app/login.html')





