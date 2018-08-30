from tastypie.resources import ModelResource
from app.models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db import models
from tastypie.models import create_api_key
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, Authentication, MultiAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import tastypie
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError


# class CustomPassWordAuthorization(Authorization):

# #auto create api_key when create user or login,..
api_key= models.signals.post_save.connect(create_api_key, sender=User)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        # must authorization : create profile(user+ detail)
        authorization = Authorization()
        excludes = ["password"]
        allowed_methods = ["get"]



class CreateUserResource(ModelResource):
    """
    create profie( = user + other information of user)
    """

    user = tastypie.fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'create_account'
        allowed_methods = ["post"]
        authorization = Authorization()
        # return json  when create user
        always_return_data = True


class AllProfileResource(ModelResource):
    """
    see all profile
    """

    user = tastypie.fields.OneToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'all_profile'
        allowed_methods = ["get", "put"]
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True


class MyProfileResource(ModelResource):
    """
    see and update my profile
    """

    user = tastypie.fields.OneToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'my_profile'
        allowed_methods = ["get", "put"]
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

    def get_list(self, request, **kwargs):
        kwargs["pk"] = request.user.profile.pk
        return super(MyProfileResource, self).get_detail(request, **kwargs)


class LogoutResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'settings'
        excludes = ['password']
        authentication = MultiAuthentication(ApiKeyAuthentication(), BasicAuthentication())
        authorization = Authorization()
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        from django.conf.urls import url
        from tastypie.utils import trailing_slash
        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),

            url(r"^(?P<resource_name>%s)/logout%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name="api_logout"),

        ]

    def logout(self, request, **kwargs):
        print("bắt đầu")
        """
        A new end point to logout the user using the django login system
        """
        self.method_check(request, allowed=['get'])
        print(request.user)
        if request.user and request.user.is_authenticated():
            logout(request)
            print(request.user)

            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False,
                                                  'error_message': 'You are not authenticated, %s' % request.user.is_authenticated()})

    def login(self, request, **kwargs):
        from tastypie.http import HttpUnauthorized, HttpForbidden
        from tastypie.models import ApiKey

        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # generator api_key after login
                # api  = ApiKey.objects.get(user=user)
                # gener_key = api.generate_key()
                # api.key = gener_key
                # api.save()
                print(dir(user))
                api_key = ApiKey.objects.get(user=user).key
                return self.create_response(request, {
                    "apikey ": api_key,
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,

                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)
