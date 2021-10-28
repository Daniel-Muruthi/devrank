from django.db.models.base import Model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, NewsLetterForm, CommentsForm,  UserProfileUpdateForm, UserProjectForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import  Location, UserProfile, Subscriber, Project,Comment
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
    posts = Project.show_projects().order_by('-pub_date')

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
    return render(request, 'index.html', {"posts":posts, "NLform":form, 'form':c_form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, user)
            user= form.cleaned_data.get('username')
            messages.success(request, f"Registration successfull {user}")
            return redirect('emaillogin')
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


            return redirect('profile')

        else:
            profileform = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'user': request.user,
        'profileform': profileform
    }
    return render(request, 'profileedit.html', context)
class FindProjectView(DetailView):
    model = Project
    template_name = 'projectfound.html'
    slug_field = "slug"

    form = CommentsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def project(self, request, *args, **kwargs):
        form = CommentsForm(request.POST)
        if form.is_valid():
            project = self.get_object()
            form.instance.user = request.user
            form.instance.project = project
            form.save()

            return redirect(reverse('project', kwargs={"form":form, 'slug':project.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context
    
    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(comment=self.object.id).count()
        post_comments = Comment.objects.all().filter(comment=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
        })
        return context
    




class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'createpost.html'
    slug_field = "slug"
    fields =['userpic', 'title', 'description','livelink']
    

    form= UserProjectForm
    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def projectpost(self, request, *args, **kwargs):
        form = UserProjectForm(request.POST)
        c_form = CommentsForm(request.POST)
        if form.is_valid() and c_form.is_valid():
            project = self.get_object()
            form.instance.user = request.user
            form.instance.project = project
            form.save()

            return redirect(reverse("project", kwargs={"projectform":form,"cform":c_form, 'pk':project.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context
    def get_success_url(self):
        return reverse('index')

class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project
    template_name='delete.html'
    success_url = reverse_lazy('index')


    def get_queryset(self):
        
        return Project.objects.all()


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentsForm
    template_name = 'addcomment.html'


def CommentPost(request, pk):
    project = get_object_or_404(Project)
    comments = project.comments.filter(id = pk)
    comment = None

    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.project = project
            comment.save()
            return redirect('index')

    else:
        form = CommentsForm()
    return render(request, 'addcomment.html', {'comments':comment, 'comments': comments, 'form':form, 'project':project})

    # form= CommentsForm
    # def form_valid(self, form):
    #     form.instance.name = self.request.user
    #     return super().form_valid(form)

    # def commentpost(self, request, id, *args, **kwargs):
    #     form = CommentsForm(request.POST)
    #     if form.is_valid():
    #         project = self.get_object(id=id)
    #         form.instance.user = request.user
    #         form.instance.project = project
    #         form.save(commit=False)

    #         return redirect("addcomment", kwargs={"form":form})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = self.form
    #     return context
    # def get_success_url(self):
    #     return reverse('findpost')

    # def projectpost(self, request, *args, **kwargs):
    #     form = CommentsForm(request.POST)
    #     if form.is_valid():
    #         project = self.get_object()
    #         form.instance.user = request.user
    #         form.instance.project = project
    #         form.save()

    #         return redirect(reverse("addcomment", kwargs={"form":form, 'pk':project.id}))

    # def get_queryset(self):
        
    # return Comment.objects.all()
