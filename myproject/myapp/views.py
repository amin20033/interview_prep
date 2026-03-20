from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import requests
import re
from .models import User,History
from django.contrib.auth import authenticate,login,logout

def ask_ai(role,experience):
    API_URL = "http://localhost:11434/api/chat"
    prompt = f"""
You are an interview preparation assistant.

Generate exactly 3 interview questions and answers for the role: {role} with experience level: {experience}.

Rules:
- One Easy, one Medium, one Hard question
- Keep answers short (2-3 sentences)
- Total response must be under 200 words

Format:

Easy
Question:
Answer:

Medium
Question:
Answer:

Hard
Question:
Answer:
"""
    payload = {
        "model": "llama3.2:1b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"
    data = response.json()
    return data["message"]["content"]

def format_ai_response(text):
    difficulties = ["Easy", "Medium", "Hard"]
    result = []

    for i, diff in enumerate(difficulties):

        pattern = rf"{diff}(.*?)(?={'|'.join(difficulties[i+1:]) if i < 2 else '$'})"
        match = re.search(pattern, text, re.S)

        if match:
            section = match.group(1).strip()
            section = section.replace("Q:", "").replace("A:", "")
            section = section.replace("Question:", "").replace("Answer:", "")
            lines = [line.strip() for line in section.split("\n") if line.strip()]
            if len(lines) >= 2:
                question = lines[0]
                answer = " ".join(lines[1:])
                result.append({
                    "difficulty": diff,
                    "question": question,
                    "answer": answer
                })
    return result

@login_required(login_url="/")
def home(request):
    if request.method=="POST":
        job = request.POST.get("job")
        exp = request.POST.get("exp")
        if job=="" or exp=="":
            return JsonResponse({"status":"error","message":"All fields are mandatory"})
        try:
            response=ask_ai(job,exp)
            response=response.replace("**","")
            try:
                questions=format_ai_response(response)
            except:
                return JsonResponse({"status":"error","message":"Unable to generate a response. Please try again."})
            History.objects.create(user=request.user,job=job,exp=exp,response=response)
        except Exception as e:
            return JsonResponse({"status":"error","message":str(e)})
        return JsonResponse({"status":"success","message":render_to_string("formatter.html",{"questions":questions})})
    return render(request, "home.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        name=request.POST.get("name")
        if email=="" or password=="" or cpassword=="" or name=="":
            return JsonResponse({"status":"error","message":"All fields are required"})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"status":"error","message":"User already exists, Please Login now"})
        if password!=cpassword:
            return JsonResponse({"status":"error","message":"Passwords do not match"})
        User.objects.create_user(name=name,email=email,password=password)
        return JsonResponse({"status":"success","message":"User created successfully"})
    return render(request,"signup.html")

def userLogin(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        if email=="" or password=="":
            return JsonResponse({"status":"error","message":"All fields are required"})
        if not User.objects.filter(email=email).exists():
            return JsonResponse({"status":"error","message":"User do not exist, Please Signup now"})
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({"status":"success","message":"Login Successful"})
        return JsonResponse({"status":"error","message":"Invalid Password"})
    return render(request,"login.html")

@login_required(login_url="/")
def userLogout(request):
    logout(request)
    return redirect("/")
@login_required(login_url="/")
def history(request):
    histories=History.objects.filter(user=request.user)
    return render(request,"history.html",{"histories":histories})
@login_required(login_url="/")
def details(request,id):
    history=History.objects.get(id=id)
    if request.user!=history.user:
        return render(request,"unauthorized.html")
    questions=format_ai_response(history.response)
    print(questions)
    return render(request,"detail.html",{"history":history,"questions":questions})

