from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, "login.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()    
    print(pw_hash)       
    this_user = User.objects.create(name = request.POST['name'], email=request.POST['email'], username = request.POST['username'], password=pw_hash) 
    request.session['user_id'] = this_user.id
    return redirect('/main')

def login(request):
    print(request.POST)
    user = User.objects.filter(email=request.POST['email'])
    if user: 
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/main')
    messages.error(request, "Invalid login info")
    return redirect ('/')

def logout(request):
    return redirect('/')

def main(request):
    context = {
            "all_users" : User.objects.all(),
            "this_user" : User.objects.get(id=int(request.session['user_id'])),
            "all_beers" : Beer.objects.all()
        }
    return render (request, "main.html", context)

def allbeers(request):
    context = {
        "all_beers" : Beer.objects.all().order_by('-updated_at'),
        "all_users" : User.objects.all(),
        "this_user" : User.objects.get(id=request.session['user_id']),
    }
    # cost per beer = price divided by quantity
    return render(request, 'beerTable.html', context)

def beerform(request):
    return render (request, "addBeer.html")

def addBeer(request):

    user = User.objects.get(id=int(request.session['user_id']))
    brand  = request.POST['brand']
    quantity = request.POST['quantity']
    cost = request.POST['cost']
    store = request.POST['store']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    this_beer = Beer.objects.create(brand=brand, quantity=quantity, cost=cost, store=store, address=address, city=city, state=state)
    this_beer.user.add(user)
    this_beer.save()

    return redirect ('/allbeers')

def deletebeer(request, beer_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_beer = Beer.objects.get(id=beer_id)

    if this_beer.user.id != request.session['user_id']:
        return redirect ('/allbeers')

    context = {
        "beer" : Beer.objects.get(id=beer_id)
    }
    beer = Beer.objects.get(id=beer_id)
    beer.delete()

    return redirect ('/allbeers')

def editbeer(request, beer_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    this_beer = Beer.objects.get(id=beer_id)


    context = {
        "beer" : Beer.objects.get(id=beer_id)
    }

    return render(request, "editBeerForm.html", context)

def updateBeer(request, beer_id):
    context = {
        "beer" : Beer.objects.get(id=beer_id)
    }
    beer = Beer.objects.get(id=beer_id)

    beer.brand = request.POST['brand']
    beer.quantity = request.POST['quantity']
    beer.cost = request.POST['cost']
    beer.store = request.POST['store']
    beer.address = request.POST['address']
    beer.city = request.POST['city']
    beer.state = request.POST['state']
    beer.save()

    return redirect('/allbeers')

def filterform(request):
    context = {
            "all_users" : User.objects.all(),
            "this_user" : User.objects.get(id=int(request.session['user_id'])),
            "all_beers" : Beer.objects.all()
        }
    return render (request, "filterforms.html", context)

def filterstate(request):
    context ={
        "beer" : Beer.objects.all(),
        "this_beer" : Beer.objects.filter(state=request.POST['state'])
    }

    return render (request, "statefilter.html", context)

def filtercity(request):
    context = {
        "beer" : Beer.objects.all(),
        "this_beer" : Beer.objects.filter(city=request.POST['city'])
    }

    return render (request, "cityfilter.html", context)

def filterbeer(request):
    context = {
        "beer" : Beer.objects.all(),
        "this_beer" : Beer.objects.filter(brand=request.POST['beer'])
    }
    return render (request, "beerfilter.html", context)