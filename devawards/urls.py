from django.urls import path
from django.conf.urls import include, url
from django.views.generic.edit import DeleteView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import AddCommentView, DeleteProject, UserProfile, EditProfile, FindProjectView, CreateProjectView



urlpatterns=[
    url(r'^$', views.landing, name='landingpage'),
    path("index/", views.userhome, name='index'),
    url( r'^emaillogin/$',views.userlogin, name="emaillogin"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    url( r'^emailsignup/$',views.signup, name="emailsignup"),
    path('profile/', views.UserProfile, name='profile' ),
    path ('profile/update/', views.EditProfile, name="update"),
    path ('project/new/', CreateProjectView.as_view(), name="newerpost"),
    path('project/<int:pk>/', views.FindProjectView.as_view(), name='findpost'),
    path('project/<int:pk>/deletepost/', DeleteProject.as_view(), name='delete'),
    path('project/<int:pk>/addcomment/', views.CommentPost, name='addcomment'),
]



if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)