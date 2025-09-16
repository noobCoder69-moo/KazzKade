from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        'self', related_name='following', symmetrical=False, blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    def followers_count(self):
        return self.followers.count()
    def following_count(self):
        return self.following.all().count
    

class Post(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like')

    def __str__(self):
        return f'{self.user.username}: {self.text[:20]}'


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like')
    
    def __str__(self):
        return f'{self.user.username} on "{self.post.text[:20]}": {self.text[:30]}'
    


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = (
            'user',
            'content_type',
            'object_id'
        )

    def __str__(self):
        return f'{self.user.username} liked {self.content_object}'
    
