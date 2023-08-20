from django.contrib import admin
from .models import CustomUser,Friends_Request,Chat

class CustomUser_Admin(admin.ModelAdmin):
  list_display = ("id","username","email",)

class Friends_Request_Admin(admin.ModelAdmin):
  list_display = ("id","request_sender", "request_receiver", "is_accepted",)
  
class Chat_Admin(admin.ModelAdmin):
  list_display = ("id","sender","receiver","timestamp")
  
admin.site.register(CustomUser,CustomUser_Admin)

admin.site.register(Friends_Request,Friends_Request_Admin)

admin.site.register(Chat,Chat_Admin)

