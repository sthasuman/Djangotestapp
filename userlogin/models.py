from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User,related_name="sender")
    receiver = models.ForeignKey(User,related_name="receiver")
    message = models.TextField()
    time_sent = models.DateTimeField(auto_now=False, auto_now_add=True)

class Notice(models.Model):
    notice_text = models.TextField()
    time_added = models.DateTimeField(auto_now=False, auto_now_add=True)

class Blog(models.Model):
    blog_title = models.TextField()
    blog_text = models.TextField()
    time_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    blog_publisher = models.ForeignKey(User,related_name="blog_publisher")

    def __str__(self):
        return self.blog_title

class BlogLike(models.Model):
    like_blog = models.ForeignKey(Blog, related_name="like_blog")
    like_done = models.ForeignKey(User,null=True,related_name="like_done")
    time_liked = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.like_blog.blog_title





