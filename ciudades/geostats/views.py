from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login as do_login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def login_view(request):
    args = {}
    if request.GET.get("no_user"):
        args['no_user'] = True
    return render(request, 'login.html', args)


def do_login_view(request):
    username = request.POST['uname']
    password = request.POST['pswd']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/admin")
    else:
        return redirect("/login?no_user=true")


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def test1(request):
    return render(request, 'test1.html')


def test2(request):
    return render(request, 'test2.html')