from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction_listing, Watchlist, NewListingForm


def index(request):
    listings = Auction_listing.objects.filter(is_done=False)

    print(listings)
    
    return render(request, "auctions/index.html", {
        'listings': listings
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        # if this is a POST request, process the form data
        form = NewListingForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            
            # process the data in form.cleaned_data as required
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]

            # Add the listing to the listings database
            new = Auction_listing(created_by=request.user, title=title, description=description, starting_bid=price, image=image)
            new.save()
        return redirect("/")

    else:
        return render(request, "auctions/create_listing.html", {
            'page_form': NewListingForm()
        })


def listing(request, id):
    listing = Auction_listing.objects.get(id = id)
    
    return render(request, "auctions/listing.html", {
        'listing': listing
    })


@login_required
def watchlist(request):
    # Get all the listing ids current user is watching
    listing_ids = Watchlist.objects.filter(user_id=request.user).values('auction_id')
    count = Watchlist.objects.filter(user_id=request.user).values('auction_id').count()
    
    # Fill a list of all the listings being watch
    auction_listings = []
    for i in range(count):
        auction_listings.append(Auction_listing.objects.filter(id=listing_ids[i]["auction_id"]))
    
    listings = []
    for i in range(count):
        for listing in auction_listings[i]:
            listings.append(auction_listings[i][0])
            print(listings)
    # Return html page with all listings being watched by user
    return render(request, "auctions/watchlist.html", {
        'listings': listings
    })


@login_required
def add_watchlist(request, id):
    # Add listing to the watchlist
    add_listing = Watchlist(auction_id=Auction_listing.objects.get(id = id), user_id=request.user)
    add_listing.save()

    # Redirect to the watchlist
    return redirect("/watchlist")


@login_required
def remove_watchlist(request, id):
    # Add listing to the watchlist
    Watchlist.objects.filter(auction_id=Auction_listing.objects.get(id = id), user_id=request.user).delete()

    # Redirect to the watchlist
    return redirect("/watchlist")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
