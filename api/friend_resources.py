from tastypie.resources import ModelResource
from app.models import Profile,Post,Comment,Friend
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
from api.authentication_custom import PostObjectsOnlyAuthorization,UserObjectsOnlyAuthorization

#get all
#request --> add(user and other user)
#denided(reset)--> add(user and other user)
#accept--> add(user and other user)
class FriendRequestResource(ModelResource):
    user = tastypie.fields.ForeignKey(UserResource, 'user')
    friend =tastypie.fields.ForeignKey(UserResource, 'friend')
    class Meta:
        queryset = Friend.objects.all()
        resource_name = "friends"
        
        authentication = ApiKeyAuthentication()
        allowed_methods = ["get","post","put","delete"]
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True

        
        
        
        
        

