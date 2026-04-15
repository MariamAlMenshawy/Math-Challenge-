from django.shortcuts import render
from  django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.

User = get_user_model()

def home(request):
    top_players = User.objects.order_by('-points')[:10]
    return render(request,'home.html',{'top_players': top_players})

@login_required 
def levels_Screen(request):
   
    return render(request,'levels.html')