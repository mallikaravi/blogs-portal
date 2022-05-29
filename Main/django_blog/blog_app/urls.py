
from django.conf.urls import url
from blog_app import views
#from blog_app.views import AddPostView
from blog_app.views import  ArticleDetailView
app_name = 'blog_app'

urlpatterns = [
    
    url(r'^register/$', views.register, name="registration"),
    url(r'^login/$', views.user_login, name="user_login"),
    url(r'^addpost/$', views.addpost, name="addpost"),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name="article"),
    url(r'^editpost/(?P<id>[0-9]+)/$', views.editpost, name="editpost"),
    url(r'^deletepost/(?P<id>[0-9]+)/$', views.deletepost, name="deletepost"),
    url(r'^editprofile/$', views.editprofile, name="editprofile"),
    url(r'^searchpost/$', views.searchpost, name="searchblog"),

]