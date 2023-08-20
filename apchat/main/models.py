from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    Facebook=models.CharField(max_length=150,null=True,blank=True)
    Instagram=models.CharField(max_length=150,null=True,blank=True)
    Twitter=models.CharField(max_length=150,null=True,blank=True)
    friends=models.ManyToManyField("CustomUser", verbose_name=("Friends"),blank=True)


class Friends_Request(models.Model):
    id=models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    request_sender=models.ForeignKey(CustomUser,related_name="sender",on_delete=models.CASCADE)
    request_receiver=models.ForeignKey(CustomUser,related_name="receiver",on_delete=models.CASCADE)
    is_accepted=models.BooleanField(default=False)
    
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    sender = models.ForeignKey(CustomUser, related_name="chat_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="chat_receiver", on_delete=models.CASCADE)
    message = models.CharField(max_length=1000, null=True, blank=True)
    thread_name = models.CharField(null=False, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sender} to {self.receiver}: {self.message}"
    
