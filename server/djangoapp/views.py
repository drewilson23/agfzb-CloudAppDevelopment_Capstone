from io import DEFAULT_BUFFER_SIZE
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        # check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New User") 
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://48cb0d67.us-south.apigw.appdomain.cloud/api/dealership/get_dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://48cb0d67.us-south.apigw.appdomain.cloud/api/dealership/get_dealerships"
        dealer = get_dealer_by_id(url, dealer_id)
        
        review_url = "https://48cb0d67.us-south.apigw.appdomain.cloud/api/review/get_reviews"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
       
        context = {
                    "dealer": dealer,
                    "reviews": reviews,
                    "dealer_id": dealer_id
                    }
  
    return render(request, 'djangoapp/dealer_details.html', context)
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    # Check if user is logged in
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://48cb0d67.us-south.apigw.appdomain.cloud/api/dealership/get_dealerships"
        dealers = get_dealers_from_cf(dealer_url)
        context["dealers"] = dealers
        context["dealer_id"] = dealer_id
        # Render add_review page if request is GET
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            return render(request, 'djangoapp/add_review.html', context)

        # If request is POST add new review submission form to Cloudant
        if request.method == "POST":
            review = {}
            form = request.POST
            review["dealership"] = dealer_id
            review["name"] = request.user.first_name + ' ' + request.user.last_name
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            
            if review["purchase"]:
                review["purchase_date"] = form["purchasedate"]
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")
            else:
                review["purchase_date" ]= None
                review["car_make"] = None
                review["car_model"] = None
                review["car_year"] = None
        
            post_url = "https://48cb0d67.us-south.apigw.appdomain.cloud/api/review/post_review"
            json_payload = {"review": review}
            post_request(post_url, json_payload, dealer_id=dealer_id)
            
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
            return redirect("/djangoapp/login")
           