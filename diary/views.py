
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .models import DiaryEntry
from textblob import TextBlob


# 1. The Writing Page (The "Desk")
@login_required(login_url='login')
def index(request):
    mood_result = None
    user_text = ""
    
    if request.method == "POST":
        user_text = request.POST.get("content")
        blob = TextBlob(user_text)
        
        if blob.sentiment.polarity > 0.1:
            mood_result = "Positive 😊"
        elif blob.sentiment.polarity < -0.1:
            mood_result = "Negative 😔"
        else:
            mood_result = "Neutral 😐"
            
        DiaryEntry.objects.create(user=request.user, content=user_text, sentiment=mood_result)
        # Optional: redirect to history after saving, or stay here to show the result
    
    return render(request, 'diary/index.html', {
        'mood': mood_result, 
        'text': user_text,
    })

# 2. The History Page (The "Library")
@login_required(login_url='login')
def history_view(request):
    query = request.GET.get('q') # Get the search word from the URL
    if query:
        # Filter entries that contain the search word
        history = DiaryEntry.objects.filter(user=request.user, content__icontains=query).order_by('-date_created')
    else:
        history = DiaryEntry.objects.filter(user=request.user).order_by('-date_created')
        
    return render(request, 'diary/history.html', {'history': history, 'query': query})
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        sec_answer = request.POST.get('security_answer')
        if form.is_valid() and sec_answer:
            user = form.save()
            UserProfile.objects.create(user=user, security_answer=sec_answer)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'diary/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'diary/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')
def reset_password_view(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        answer = request.POST.get('answer')
        new_pw = request.POST.get('new_password')
        
        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
            
            if profile.security_answer.lower() == answer.lower():
                user.set_password(new_pw)
                user.save()
                return redirect('login')
            else:
                message = "Wrong answer! Try again."
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            message = "User not found."
            
    return render(request, 'diary/reset_password.html', {'message': message})