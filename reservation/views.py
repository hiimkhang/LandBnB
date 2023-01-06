import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from house import models as house_models
from review import forms as review_forms
from . import models

class CreateError(Exception):
    pass

def create(request, house, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        house = house_models.House.objects.get(pk=house)
        models.BookedDay.objects.get(day=date_obj, reservation__house=house)
        raise CreateError()
    except (house_models.House.DoesNotExist, CreateError):
        messages.error(request, "Can't book this house")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            house=house,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.house.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        context = {"reservation": reservation, "form": form}
        return render(self.request, "reservation/detail.html", context)


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.house.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))