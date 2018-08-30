# luu vao file word cac buoc chi chi
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birthday = models.DateField()
    address = models.CharField(max_length=100)

    @property
    def full_name(self):
        "Returns the user's full name."
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        """
            save user have encrypted password
        """
        user = User.objects.get(username=self.user.username)
        user.set_password(user.password);
        user.save()

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.full_name)


class Friend(models.Model):
    """
    status of friends
        0: reset status
        1: is a request friend
        2: accept  friend

    """
    STATUS_FRIEND = (
        ('0', 'reset_request'),
        ('1', 'is_request'),
        ('2', 'accept_friend'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")
    status = models.CharField(max_length=1, choices=STATUS_FRIEND)
    """
    is a friend: check 
        0:not a friend
        1: a friend
    """
    is_friend = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class Post(models.Model):
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # count of like in this  post
    count_like = models.IntegerField(default=0)
    # count of comment in this  post
    count_comment = models.IntegerField(default=0)

    def __str__(self):
        return '%s . %s' % (str(self.id), self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)
