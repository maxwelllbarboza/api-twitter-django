from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Follow(models.Model):        
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"    
        



