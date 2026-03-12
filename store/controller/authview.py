from django.contrib.auth import  authenticate,login,logout
from django.shortcuts import redirect,render
from django.contrib import  messages
from  store.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered successfully! Login to continue!")
            return redirect('/login')
    context = {'form': form}
    return render(request,"store/auth/register.html",context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request,"Your are already logged in!")
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST.get('Username')
            passwd = request.POST.get('Password')
            user = authenticate(request,username=name,password=passwd)

            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid username & password!")
                return redirect('/login')
    return render(request,"store/auth/login.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully!")
    return redirect('/')