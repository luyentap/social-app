from tastypie.resources import ModelResource
from app.models import Profile, Post, Comment
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, Authentication, MultiAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import tastypie
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
# fix import with python3
from api.account_resources import *
from api.authentication_custom import PostObjectsOnlyAuthorization


class PostByUserResource(ModelResource):
    """
        User can: create post, update and delelte
                  also see all post of user
    """
    author = tastypie.fields.ForeignKey(UserResource, 'author')

    class Meta:
        resource_name = 'my_post'
        queryset = Post.objects.all()
        method_allow = ["get", "put", "delete", "post"]
        authentication = ApiKeyAuthentication()
        authorization = PostObjectsOnlyAuthorization()
        always_return_data = True


class AllPostsResource(ModelResource):
    """
    get all post (show in wall)
    and use it in other resources
    """

    class Meta:
        resource_name = 'all_post'
        queryset = Post.objects.all()
        method_allow = ["get"]
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class ListPostByOtherUserResource(ModelResource):
    """
    Get to list post by other user
        example: api/v1/list_post/user/12 --> list post of user id=12
    
    """

    author = tastypie.fields.ForeignKey(UserResource, 'author')

    class Meta:
        resource_name = 'list_post'
        queryset = Post.objects.all()
        method_allow = ["get"]
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        from django.conf.urls import url
        return [

            url(r"^(?P<resource_name>%s)/user/(?P<id_user>[\w\d_.-]+)" % self._meta.resource_name,
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),

        ]

    def dispatch_list(self, request, **kwargs):
        return self.get_list(request, **kwargs)

    def authorized_read_list(self, object_list, bundle):
        # print(bundle.request.path)
        id_user = bundle.request.resolver_match.kwargs["id_user"]
        return object_list.filter(author=id_user).select_related()

    def get_list(self, request, **kwargs):
        return super(ListPostByOtherUserResource, self).get_list(request, **kwargs)
