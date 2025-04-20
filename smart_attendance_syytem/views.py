# from django.shortcuts import render,redirect,HttpResponse
# from myapp.EmailBackEnd import EmailBackEnd
# from django.contrib.auth import authenticate,login,logout

# def BASE(request):
#     return render(request,'base.html')

# def LOGIN(request):
#     return render(request,'login.html')

# def dologin(request):
#     if request.method == "POST":
#     #if request.method == "post":

#         user = EmailBackEnd.authenticate(request,
#                                          username=request.POST.get('email'),
#                                          password=request.POST.get('password'),)
#         if user!=None:
#             login(request.user)
#             user_type = user.user_type
#             if user_type == '1':
#                 return HttpResponse("hod panel")
#             elif user_type == '2':
#                 return HttpResponse("teacher panel")
#             elif user_type == '3':
#                 return HttpResponse("student panel")
#             else:
#                 #message
#                 return redirect("login")
#         else:
#             #message
#             return redirect("login")
from django.shortcuts import render, redirect, HttpResponse
from myapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.models import CustomUser

def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')

def dologin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = EmailBackEnd.authenticate(request, username=email, password=password)

        if user is not None:
            # Login the authenticated user
            login(request, user)

            user_type = user.user_type
            if user_type == '1':
                #return render(request, 'hod/home.html')
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:
                messages.error(request,"Email and password are invalid!")
                return redirect("login")
        else:
            messages.error(request,"Email and password are invalid!")
            return redirect("login")
            
def dologout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html',context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
       #email = request.POST.get('email')
       #username = request.POST.get('username')
        password = request.POST.get('password')
        #print(profile_pic)
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            if password :
                customuser.set_password(password)
            #if profile_pic :
                 #customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"your profile update successfully")
            return redirect("profile")
  
        except:
            messages.error(request, "your profile update failed")
            
    return render(request, 'profile.html')