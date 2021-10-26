from django.contrib import admin
from .models import Location,UserProfile, Comment, Subscriber, Project , ProjectRating
from django.contrib.admin import AdminSite


admin.site.register(Location)
admin.site.register(Project)
admin.site.register(ProjectRating)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Subscriber)