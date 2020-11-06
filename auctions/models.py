from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.forms import MultiWidget, TextInput


class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.URLField(label="Image URL", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    id = models.AutoField(primary_key = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Listing {self.id}: {self.title}, selling for ${self.starting_bid}"


class Bid(models.Model):
    id = models.AutoField(primary_key = True)
    auction_id = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="bids")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_sum = models.DecimalField(max_digits=6, decimal_places=2)


class Comment(models.Model):
    id = models.AutoField(primary_key = True)


class Watchlist(models.Model):
    id = models.AutoField(primary_key = True)
    auction_id = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="watchlist")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")