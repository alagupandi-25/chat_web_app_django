import json
from django.template import loader
from django.contrib import messages
from .forms import UserRegisterForm
from django.core.paginator import Paginator
from .models import CustomUser,Friends_Request,Chat
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,Http404
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import redirect,render,get_object_or_404


@login_required
def Search_contact(request):
   
   query=request.GET.get('query')
   current_username=request.user.username
   user_object = CustomUser.objects.filter(username__contains=query).exclude(username=current_username)[:20] 

   if user_object is not None:
    data=[
        {
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'image': obj.image.url if obj.image else None,
        }
        for obj in user_object
        ]
    
   else:
      data=[]

   return JsonResponse(data,safe=False)


@login_required
def update_user_data(request):

    try:
        jsondata = json.loads(request.body)
        username = jsondata.get('username')
        user_object = CustomUser.objects.get(username=username)

        user_object.username = jsondata.get('username')
        user_object.first_name = jsondata.get('firstname')
        user_object.last_name = jsondata.get('lastname')
        user_object.email = jsondata.get('email')
        user_object.phone_number = jsondata.get('phonenumber')
        user_object.Facebook = jsondata.get('facebook')
        user_object.Instagram = jsondata.get('instagram')
        user_object.Twitter = jsondata.get('twitter')
        user_object.save()

        data = {
            'status': 'success'
        }

    except json.JSONDecodeError:
        data = {
            'status': 'error'
        }

    except CustomUser.DoesNotExist:
        data = {
            'status': 'error',
            'message': 'User not found'
        }

    return JsonResponse(data, safe=True)


@login_required
def Index(request):
  
  template = loader.get_template('index.html')
  user_object=request.user
  
  context={
     'user_object':user_object
  }
  
  return HttpResponse(template.render(context))



def Register(request):  
  
  form = UserRegisterForm()  

  if request.method == 'POST':  
      form = UserRegisterForm(request.POST or None) 

      if form.is_valid():  
          user=form.save()
          login(request, user) 
          return redirect('index')
      
      else:
          messages.error(request, 'Invalid form submission.')
          messages.error(request, form.errors)

  context = {'form':form}  
  return render(request,'register.html',context)


@login_required
def Account(request):
   
   user_object=request.user
 
   context={
      'user_object':user_object,
      }
   
   request_list=Friends_Request.objects.filter(request_receiver=user_object)

   if request_list.exists():
      context["request_list"]=request_list

   return render(request,'settings.html',context)

@login_required
def update_image(request):
   
   if request.method == "POST":
      
      user_object=request.user
      image_file=request.FILES.get('image_file')
      user_object.image=image_file
      user_object.save()
      data={
         'status': 'success',
         'userimage':user_object.image.url
      }

   else:
      data = {
            'status': 'error'
      }

   return JsonResponse(data,safe=True)

   
def Login(request):
   
   form=AuthenticationForm()

   if request.method=="POST":
      form=AuthenticationForm(request,data=request.POST)

      if form.is_valid():
         user_name=form.cleaned_data.get('username')
         user_password=form.cleaned_data.get('password')
         user=authenticate(username=user_name,password=user_password)

         if user is not None:
            login(request, user)
            return redirect('index')
         else:
            messages.error('Invalid user')
         
      else:
         messages.error(request, 'Invalid form submission.')
         messages.error(request, form.errors)

   context={'form':form}
   return render(request,'login.html',context)


@login_required
def User_profile(request,username):

   user_profile=get_object_or_404(CustomUser,username=username)
   current_user=request.user

   if user_profile.username !=current_user.username:

      is_friend = current_user.friends.filter(pk=user_profile.id).exists()
      is_received_request = Friends_Request.objects.filter(request_sender=current_user,request_receiver=user_profile,).exists() 
      is_accepted = Friends_Request.objects.filter(request_sender=user_profile,request_receiver=request.user,is_accepted=True).exists()

      context={
               'user_profile':user_profile,
               'is_friend':is_friend,
               'is_received_request':is_received_request,
               'is_accepted':is_accepted
            }
      
      return render(request,'profile.html',context)

   else:
      return redirect('settings')
   

@login_required
def Logout(request):

   logout(request)
   return redirect('login')


@login_required
def Friend_info(request):

   user_profile_name=request.GET.get('username')

   user_profile=get_object_or_404(CustomUser,username=user_profile_name)
   current_user=request.user

   if user_profile.username !=current_user.username:

      is_friend = current_user.friends.filter(pk=user_profile.id).exists()
      is_received_request = Friends_Request.objects.filter(request_sender=current_user,request_receiver=user_profile,).exists() 
      is_accepted = Friends_Request.objects.filter(request_sender=user_profile,request_receiver=request.user,is_accepted=True).exists()

      data={
            'is_friend':is_friend,
            'is_received_request':is_received_request,
            'is_accepted':is_accepted,
         }
      
      if is_received_request == True:
         data["request_id"]=Friends_Request.objects.filter(request_sender=current_user,request_receiver=user_profile)[0].id
         
      return JsonResponse(data,safe=True)

   else:
      return redirect('settings')
   
@login_required
def Sent_request(request):

   user_profile_name=request.POST.get('username')

   current_user=request.user
   user_profile=get_object_or_404(CustomUser,username=user_profile_name)

   object,created=Friends_Request.objects.get_or_create(request_sender=current_user,request_receiver=user_profile)
   
   if created:
      data={
         'status': 'success',
         'request_id':object.id,
      }
      
   else:
      data = {
            'status': 'error'
      }
   
   return JsonResponse(data,safe=True)

@login_required
def Cancel_request(request):

   try:
      request_id=request.POST.get('request_id')

      request_object=get_object_or_404(Friends_Request,id=request_id)
      request_object.delete()

      data = {
         'status': 'success',
      }

   except:
      data = {
            'status': 'error'
      }
   
   return JsonResponse(data,safe=True)

@login_required
def Accept_request(request):

    try:
        request_id = request.POST.get('request_id')
        request_object = get_object_or_404(Friends_Request, id=request_id)

        if request_object.request_receiver == request.user:
            request_object.request_sender.friends.add(request_object.request_receiver)
            request_object.request_receiver.friends.add(request_object.request_sender)
            request_object.delete()

            data = {
                'status': 'success',
            }

        else:

            data = {
                'status': 'error',
            }

    except Exception:

        data = {
            'status': 'error',
        }

    return JsonResponse(data, safe=True)
 
@login_required
def Chat_page(request,user_name):
   
   user_object=request.user
   other_user=get_object_or_404(CustomUser,username=user_name)
   
   if not other_user in  user_object.friends.all():
      raise Http404("The user does not exist.")
   
   if int(user_object.id) > int(other_user.id):
      thread_name = f'{user_object.id}-{other_user.id}'
   else:
      thread_name = f'{other_user.id}-{user_object.id}'
            
   message_obj = Chat.objects.filter(thread_name=thread_name).order_by("timestamp")
   
   context={
         'user_object':user_object,'other_user':other_user,'message_obj':message_obj
      }
   
   return render(request,'chat.html',context)

 
   
   