"""socialapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from api.account_resources import *
from api.post_resources import *
from  api.friend_resources import *
from api.like_resources import *
from api.comment_resources import *
from tastypie.api import Api

#define api and register resources
#user and profile
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(CreateUserResource())
v1_api.register(AllProfileResource())
v1_api.register(MyProfileResource())
# v1_api.register(LoginResource())
v1_api.register(LogoutResource())

#register api : post
v1_api.register(PostByUserResource())
v1_api.register(AllPostsResource())
v1_api.register(ListPostByOtherUserResource())

#register api : friend
v1_api.register(FriendRequestResource())

#register api: like post
v1_api.register(LikePostResource())
v1_api.register(AllLikeInPostResource())

#register api: comment post
v1_api.register(CommentInPostResource())
v1_api.register(AllCommentInPostResource())


#define patterns of url
urlpatterns = [
    # url("^api/ ^(?P<api_name>v1)/$ [name='api_v1_top_level']",none),
    url(r'^admin/', admin.site.urls),
    url('/app/',include('app.urls')),
    url(r'^api/', include(v1_api.urls)),
    
]



