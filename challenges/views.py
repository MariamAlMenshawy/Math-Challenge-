from datetime import datetime, timedelta 
from django.utils import timezone

from django.shortcuts import redirect, render,get_object_or_404
from  django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Session,Question
import random

# Create your views here.

User = get_user_model()

def home(request):
    top_players = User.objects.order_by('-points')[:5]
    return render(request,'home.html',{'top_players': top_players})

@login_required 
def levels_Screen(request):
    if request.method == "POST":
        session = Session.objects.create(
            user_id=request.user,
            created_at=timezone.now(),
            level=request.POST.get('level')
        )
        return redirect('solve_session', session_id=session.pk)
    
    return render(request,'levels.html')

def solve_session(request,session_id):
     
    session = get_object_or_404(Session,pk=session_id)

    if str(request.session.get("current_session")) != str(session_id) :  # لو new session
        request.session["index"] = 0
        request.session["start_time"] = timezone.now().isoformat()
        request.session["current_session"] = session_id
        request.session["question_id"] = None
        request.session["equation"] = None

    index = request.session.get("index", 0)
    start_time = datetime.fromisoformat(request.session["start_time"])
    time2 = start_time + timedelta(seconds=session.time)
    now = timezone.now()
    remaining = (time2 - now).total_seconds()
    operators = ["+", "-", "*", "/"]

    if request.method == "GET":
        question_id = request.session.get("question_id")

        if not question_id:
            q = Question()
            q.session_id = session
            q.created_at = timezone.now()
            q.equation = ""

            if session.level == 'easy' :
                numbers = 2
            elif session.level == 'medium' :
                numbers = 3
            else :
                numbers = 4

            for i in range(numbers):
                num = random.randint(1,20)
                q.equation += str(num)

                if i < (numbers - 1) : 
                    op = random.choice(operators)
                    q.equation += " " + op + " "
            
            q.save()
            request.session['question_id'] = q.id
            request.session['equation'] = q.equation
    
        else:
            q = get_object_or_404(Question, id=question_id)

        return render(request, 'solve_session.html',{'index': index,'question': q,'session': session,'remaining_time': int(remaining if remaining > 0 else 0)})


    else:   # POST
        question_id = request.session.get("question_id")
        if not question_id:
            return redirect('levels')
        q = get_object_or_404(Question, id=question_id)

        try:
            q.user_answer = float(request.POST.get('user_answer'))
        except:
            q.user_answer = None

        try:
            q.correct_answer = round(eval(q.equation),2)
        except ZeroDivisionError:
            q.correct_answer = 0
        
        q.save()

        request.session["index"] += 1 
        request.session.pop("question_id", None)
        request.session.pop("equation", None)
        
        if timezone.now() >= time2 or request.session["index"] >= 5 :
            session.complete_session()

            for key in ["index", "start_time", "current_session", "equation", "question_id"]:
                request.session.pop(key, None)

            return redirect('result', session_id=session.pk)
        
        return redirect('solve_session',session_id=session_id)

        
        
def result(request,session_id):
    session = get_object_or_404(Session,pk=session_id)
    return render(request,"result.html",{'session':session})

       
def history(request):
    sessions = Session.objects.filter(user_id=request.user).order_by('-created_at')
    return render(request,'history.html',{'sessions':sessions})