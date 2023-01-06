from django.contrib import messages
from django.shortcuts import redirect, reverse
from house import models as house_models
from . import forms


def create_review(request, house):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        house = house_models.House.objects.get_or_none(pk=house)
        if not house:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.house = house
            review.user = request.user
            review.save()
            messages.success(request, "House has been reviewed")
            return redirect(reverse("houses:detail", kwargs={"pk": house.pk}))