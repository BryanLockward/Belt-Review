from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
import re
from .models import User
import bcrypt
from django.contrib import messages
from ..review.models import Book




def index(request):
    return render(request, 'login/index.html')

def login(request):
    user={}
    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            user[key]=value

    errors = User.objects.validate_login(user)
    if len(errors)>0:
        messages.error(request, errors)
        return redirect('/')
    request.session['email'] = user['email']
    return HttpResponseRedirect(reverse("review:index"))

def register(request):
    new_user={}
    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            new_user[key]=value
    errors = User.objects.validate_registration(new_user)
    if errors:
        for message in errors:
            messages.error(request, message)
        return redirect('/')


    hashed = bcrypt.hashpw((new_user['password'].encode()), bcrypt.gensalt(5))
    User.objects.create(
        name=new_user['name'],
        user_name=new_user['user_name'],
        email=new_user['email'],
        password=hashed
        )
    messages.success(request, "Successfully registered! Please Login Now")
    return redirect('/')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


def show(request, user_id):
    user = User.objects.get(id=user_id)
    book_ids = user.reviews_left.all().values("book").distinct()
    user_books = []
    for book in book_ids:
        user_books.append(Book.objects.get(id=book['book']))
    context = {
        'user': user,
        'unique_book_reviews': user_books
    }
    return render(request, 'login/show.html', context)
