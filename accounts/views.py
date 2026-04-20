from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from accounts.models import User
from .forms import SignUpForm
from django.contrib.auth import login as auth_login, logout 
from django.views.generic import UpdateView

# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form  = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth_login(request,user)

            return redirect('home')
        
    return render(request,'signup.html',{'form':form})

def logOut(request):
    logout(request)
    return redirect('home')

        
class UpdateProfileInfo(UpdateView):
    model = User
    fields = ('profile_image','full_name','email')
    template_name = 'profile_info.html'
    success_url = reverse_lazy('home')

    def get_object(self):    
        return self.request.user
