from django.db.models.base import Model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, NewsLetterForm, CommentsForm,  UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import  Location, UserProfile, Subscriber, Project
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView,UpdateView, CreateView, DeleteView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def landing(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, "Registration successfull")
            return redirect("cloneapp:index.html")
        messages.error(request, "Unsuccessful registration. Invalid Information")
    form = SignUpForm()
    return render(request, 'landing.html', context={"signup_form":form})


@login_required(login_url='/emaillogin/')
def  userhome(request):
    # posts = Post.show_posts().order_by('-pub_date')

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        c_form = CommentsForm(request.POST)
        if form.is_valid() and c_form.is_valid():
            name=form.cleaned_data['your_name']
            email=form.cleaned_data['email']
            recipient = Subscriber(name=name, email=email)
            recipient.save()
            # -------------------------
            comment=c_form.cleaned_data['comment']
            c_form.save()
            HttpResponseRedirect('userhome')
    else:
        form =NewsLetterForm()
        c_form = CommentsForm(request.POST)
    return render(request, 'index.html', { "NLform":form, 'form':c_form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, user)
            user= form.cleaned_data.get('username')
            messages.success(request, f"Registration successfull {user}")
            return redirect('cloneapp:emaillogin')
        else:
            messages.error(request, "Unsuccessful registration. Invalid Information")
            return render(request, "registration/registration_form.html", {"signup_form":form})
    else:
        form = SignUpForm()
        return render(request, "registration/registration_form.html",{"signup_form":form})

def userlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
                return render(request, 'registration/registration_form.html')

        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "registration/login.html",{"emaillogin_form":form})

def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/landingpage/')



def UserProfile(request):
    profileform = UserProfileUpdateForm(instance=request.user.userprofile)
    if request.method == 'POST':
        profileform=UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if profileform.is_valid():
            profileform.save(commit=False)

            return redirect('cloneapp:profile')

        else:
            profileform = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user': request.user,
        'profileform': profileform
    }
    return render(request, 'profile.html', context)


def EditProfile(request):
    profileform = UserProfileUpdateForm(instance=request.user.userprofile)
    if request.method == 'POST':
        profileform=UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if profileform.is_valid():
            profileform.save(commit=False)


            return redirect('cloneapp:profile')

        else:
            profileform = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user': request.user,
        'profileform': profileform
    }
    return render(request, 'profileedit.html', context)


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'createpost.html'
    slug_field = "slug"
    fields =['userpic', 'description','livelink']

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def projectpost(self, request, *args, **kwargs):
        form = UserProjectForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse("post", kwargs={"commentform":form, 'slug':post.slug}))


