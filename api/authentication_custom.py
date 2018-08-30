from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class PostObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(author=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.author == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.author == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class LikeObjectsOnlyAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        return bundle.obj.liker == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.liker == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.liker == bundle.request.user


class CommentObjectsOnlyAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        return bundle.obj.commenter == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.commenter == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.commenter == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed
