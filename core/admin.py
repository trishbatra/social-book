from django.contrib import admin
from .models import profile,post,likedpost,followersCount
# Register your models here.
admin.site.register(profile)
admin.site.register(post)
admin.site.register(likedpost)
admin.site.register(followersCount)