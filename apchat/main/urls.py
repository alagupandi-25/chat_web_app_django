from django.urls import path
from main.views import *

urlpatterns = [
    
     path('' , Index , name="index"),
     path('login',Login,name='login'),
     path('logout',Logout,name="logout"),
     path('settings',Account,name="settings"),
     path('signup' , Register , name="register"),
     path('<user_name>',Chat_page,name="chatpage"),
     path('friendinfo',Friend_info,name="Friendinfo"),
     path('updateimage',update_image,name='updateimage'),
     path('sentrequest',Sent_request,name="sent_request"),
     path('/getcontact', Search_contact ,name="getcontact"),
     path('updateuser',update_user_data,name="updateuser"),
     path('acceptrequest',Accept_request,name="acceptrequest"),
     path('cancelrequest',Cancel_request,name="cancelrequest"),
     path('view_profile/<username>',User_profile,name="viewprofile"),
     
]
