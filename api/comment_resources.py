from tastypie.resources import ModelResource
from app.models import Profile,Post,Comment,Friend,Like,Comment
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
from tastypie.authentication import ApiKeyAuthentication,BasicAuthentication,Authentication,MultiAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import tastypie
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
#fix import with python3
from api.account_resources import *
from api.post_resources import *
from api.autho_custom import CommentObjectsOnlyAuthorization



class CommentInPostResource(ModelResource):
    """
    comment in a post:
        create comment, update and delete
    
    """
    commenter = tastypie.fields.ForeignKey(UserResource, 'commenter')
    post = tastypie.fields.ForeignKey(AllPostsResource,'post',full=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = "comment"
        allowed_methods = ["get","post","put","delete"]
        authentication = ApiKeyAuthentication()
        authorization = CommentObjectsOnlyAuthorization()
        always_return_data = True
        
    
    def obj_create(self, bundle, **kwargs):
        """
        when comment , increate number comment in post
        """
        post = bundle.data["post"]
        id_post = post.split("/")[4]
        
        p= Post.objects.get(id=id_post)
        p.count_comment = p.count_comment+1
        p.save()
        
        return super(CommentInPostResource,self).obj_create(bundle,**kwargs)
    
    
    def obj_delete(self, bundle, **kwargs):
        """
        when delete comment , decreate number comment in post
        """
        #get id comment --> comment -->posst
        id_comment= bundle.request.resolver_match.kwargs["pk"]
        # post = bundle.request.path
        # id_post = post.split("/")[4]
        
        c = Comment.objects.get(id = id_comment)
        p = c.post
        
        #decreate number comment
        p.count_comment = p.count_comment-1
        p.save()
        
        return super(CommentInPostResource,self).obj_create(bundle,**kwargs)
    


class AllCommentInPostResource(ModelResource):
    """
    get people comment in a post 
    example :  api/v1/post/<post_id>/all_comment 
               api/v1/post/1/all_comment 
        
    """
    
    commenter = tastypie.fields.ForeignKey(UserResource, 'commenter')
    post = tastypie.fields.ForeignKey(AllPostsResource,'post')
    class Meta:
        queryset = Comment.objects.all()
        resource_name = "all_comment"
        allowed_methods = ["get"]
        authentication = ApiKeyAuthentication()
        
    def prepend_urls(self):
        from django.conf.urls import url
        return [
            url(r"^post/(?P<id_post>[\w\d_.-]+)/(?P<resource_name>%s)" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            
        ]
    
    def dispatch_list(self, request, **kwargs):
        self.is_authenticated(request)
        # self.is_authorized(request)
        return self.get_list(request, **kwargs)
     

    def authorized_read_list(self, object_list, bundle):
        id_post = bundle.request.resolver_match.kwargs["id_post"]
        return object_list.filter(post_id=id_post).select_related()
        
    def get_list(self, request, **kwargs):
        self.is_authenticated(request)  
        return super(AllCommentInPostResource, self).get_list(request, **kwargs)

        
        

    
                