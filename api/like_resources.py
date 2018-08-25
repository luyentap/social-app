from tastypie.resources import ModelResource
from app.models import Profile,Post,Comment,Friend,Like
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
from api.autho_custom import PostObjectsOnlyAuthorization,UserObjectsOnlyAuthorization,LikeObjectsOnlyAuthorization



class LikePostResource(ModelResource):
    """
        liked post, unliked
    
    """
    
    liker = tastypie.fields.ForeignKey(UserResource, 'liker')
    post = tastypie.fields.ForeignKey(AllPostsResource,'post')
    class Meta:
        queryset = Like.objects.all()
        resource_name = "like"
        allowed_methods = ["get","post","delete"]
        authentication = ApiKeyAuthentication()
        authorization = LikeObjectsOnlyAuthorization()
        always_return_data = True
    
    #when like , increate number like in post
    def obj_create(self, bundle, **kwargs):
        post = bundle.data["post"]
        id_post = post.split("/")[4]
        
        p= Post.objects.get(id=id_post)
        p.count_like = p.count_like+1
        p.save()
        
        return super(LikePostResource,self).obj_create(bundle,**kwargs)
    
    def obj_delete(self, bundle, **kwargs):
        """
        when unlike , decreate number like in post
        da unlike, giam so luong nhung return thong bao loi???
        """
        #get id like --> like -->posst
        id_like= bundle.request.resolver_match.kwargs["pk"]
        # post = bundle.request.path
        # id_post = post.split("/")[4]
        c = Like.objects.get(id = id_like)
        p = c.post
        #decreate number comment
        p.count_like = p.count_like-1
        p.save()
        
        return super(LikePostResource,self).obj_create(bundle,**kwargs)
    


class AllLikeInPostResource(ModelResource):
    """
        get people like in a post
        example :  api/v1/post/<post_id>/all_like 
                   api/v1/post/1/all_like
    """
    liker = tastypie.fields.ForeignKey(UserResource, 'liker')
    post = tastypie.fields.ForeignKey(AllPostsResource,'post')
    class Meta:
        queryset = Like.objects.all()
        resource_name = "all_like"
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
        return super(AllLikeInPostResource, self).get_list(request, **kwargs)

        
    

    
                