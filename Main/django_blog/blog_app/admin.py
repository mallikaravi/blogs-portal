from django.contrib import admin
from blog_app.models import UserProfileInfo, Post

# Register your models here.

admin.site.register(UserProfileInfo)

class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'created_on')

admin.site.register(Post, PostAdmin)

