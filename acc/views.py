from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from.models import User
from django.contrib import messages

# Create your views here.
def index(reqeust):
    return render(reqeust, 'acc/index.html')

def login_user(request):
    if request.method == 'POST':
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user :
            login(request, user)
            messages.success(request, f"{user} 님 환영합니다.")
            return redirect("acc:index")
        else:   
            messages.error(request, "아이디 또는 패스워드가 잘못되었습니다 :(")
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")

def profile(request):

    return render(request, 'acc/profile.html')

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ua = request.POST.get("uage")
        uc = request.POST.get("ucom")
        upic = request.FILES.get("uimg")
        User.objects.create_user(username=un, password=pw, age=ua, comment=uc, pic=upic)
        return redirect("acc:login")
    return render(request, 'acc/signup.html')

def delete(request):
    if check_password(request.POST.get("passcheck"), request.user.password):
        request.user.delete()
    return redirect("acc:index")

def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("upass")
        uc = request.POST.get("ucom")
        upic = request.FILES.get("uimg")
        if pw:
            u.set_password('pw')
        if upic:
            u.pic=upic
        u.comment=uc
        u.save()
        return redirect("acc:profile")
    return render(request, "acc/update.html")
