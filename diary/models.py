
from django.db import models
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)
    sentiment=models.CharField(max_length=50,blank=True,null=True)
    
    def __str__(self):
        return f"{self.user.username}'s entry on {self.date_created.strftime('%Y-%m-%d')}"

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question = models.CharField(max_length=255, default="What is your favorite color?")
    security_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Profile for {self.user.username}"