from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def index(request):
    return render(request, "log_app/index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            print(request.POST)
            fn = request.POST["fname"]
            ln = request.POST["lname"]
            em = request.POST["email"]
            pw = request.POST["pass"]
            hashpw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            newuser = User.objects.create(first_name=fn, last_name=ln, email=em, password=hashpw)
            print(newuser)
            user = User.objects.get(email=em)
            request.session["name"] = user.first_name
            request.session["id"] = user.id
            messages.success(request, 'You have succefully made an account')
            return redirect('/wall')

def login(request):
    if request.method == "POST":
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            print("email passed first validation")
            em = request.POST["email"]
            pw = request.POST["pass"]
            user = User.objects.filter(email=em)
            if not user:
                print("failed email")
                messages.error(request, 'Incorrect Login Info') 
                return redirect("/")
            else:
                print("Grabbing email from database")
                user = User.objects.get(email=em)
                if bcrypt.checkpw(pw.encode(), user.password.encode()):
                    print("password match")
                    request.session["name"] = user.first_name
                    request.session["id"] = user.id
                    messages.success(request, 'You have succefully logged in')
                    return redirect("/wall")
                else:
                    print("failed password")
                    messages.error(request, 'Incorrect Login Info') 
                    return redirect("/")

def success(request):
    if "name" not in request.session:
        messages.error(request, 'You must be logged in to access that information') 
        return redirect("/")
    else:
        context = {
            "all_messages": Message.objects.all().order_by("-created_at"),
            "all_comments": Comment.objects.all(),
        }
        return render(request, "log_app/success.html", context)

def message(request):
    if request.method == "POST":
        me = request.POST["message"]
        pid = request.POST["pageid"]
        uid = User.objects.get(id=pid)
        #print(request.POST)
        postmess = Message.objects.create(content=me, user=uid)
        print(postmess.content)
        return redirect("/wall")

def comment(request):
    if request.method == "POST":
        com = request.POST["comment"]
        pid = request.POST["pageid"]
        mid = request.POST["messid"]
        uid = User.objects.get(id=pid)
        meid = Message.objects.get(id=mid)
        postcom = Comment.objects.create(content=com, user=uid, message=meid)
        print(postcom.content)
        return redirect("/wall")

def delete(request, type, deleteid):
        if type == "comment":
            com = Comment.objects.get(id=deleteid)
            if request.session["id"] == com.user.id:
                Comment.objects.get(id=deleteid).delete()
                return redirect("/wall")
            else:
                messages.error(request, 'That does not belong to you!')
                return redirect("/")

        if type =="message":
            mess = Message.objects.get(id=deleteid)
            if request.session["id"] == mess.user.id:
                Message.objects.get(id=deleteid).delete()
                return redirect("/wall")
            else:
                messages.error(request, 'That does not belong to you!')
                return redirect("/")

        else:
            messages.error(request, 'That is illegal!')
            return redirect("/")



def logout(request):
    request.session.clear()
    return redirect('/')