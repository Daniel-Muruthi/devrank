from django.urls import path
from django.conf.urls import include, url
from django.views.generic.edit import DeleteView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import UserProfile, EditProfile



urlpatterns=[
    url(r'^$', views.landing, name='landingpage'),
    path("index/", views.userhome, name='index'),
    url( r'^emaillogin/$',views.userlogin, name="emaillogin"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    url( r'^emailsignup/$',views.signup, name="emailsignup"),
    path('profile/', views.UserProfile, name='profile' ),
    path ('profile/update/', views.EditProfile, name="update"),
    path ('post/new/', views.CreateProjectView.as_view(), name="newerpost"),

]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)