from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from . import models, forms
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_countries import countries
from users import mixin as user_mixins
from django.http import Http404

# Create your views here.

class HomeView(ListView):
    model = models.House
    paginate_by = 10
    paginate_orphans = 5
    ordering = "name"
    # ordering = "created"
    page_kwarg = "page" 
    context_object_name = "houses"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now
    #     context["now"] = now
        
    #     return context
    # pass

class HouseDetail(DetailView):
    model = models.House

class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        houses = models.House.objects.all()
        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                country = form.cleaned_data.get("country")
                city = form.cleaned_data.get("city")
                house_type = form.cleaned_data.get("house_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # search argument
                filter_args = {}
                filter_args["country"] = country
                if city != "":
                    filter_args["city__startswith"] = city
                if house_type is not None:
                    filter_args["house_type"] = house_type
                if price is not None:
                    filter_args["price__lte"] = price
                if guests is not None:
                    filter_args["guests__gte"] = guests
                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
                if beds is not None:
                    filter_args["beds__gte"] = beds
                if baths is not None:
                    filter_args["baths__gte"] = baths
                for amenity in amenities:
                    filter_args["amenities"] = amenity
                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.House.objects.filter(**filter_args)
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                houses = paginator.get_page(page)
                context = {"form": form, "houses": houses}
                return render(request, "house/search.html", context)
        else:
            form = forms.SearchForm()
            context = {"form": form}

        # context = {"form": form, "houses":houses} 

        return render(request, "house/search.html", context)

class CreateHouseView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateHouseForm 
    template_name = "house/house_create.html"

    def form_valid(self, form):
        house = form.save() 
        house.host = self.request.user  
        house.save()  
        form.save_m2m() # many 2 many
        messages.success(self.request, "House has been added")
        return redirect(reverse("houses:detail", kwargs={"pk": house.pk}))

class EditHouseView(user_mixins.LoggedInOnlyView, UpdateView): 
    model = models.House 
    template_name = "house/house_edit.html" 
    fields = ( 
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guest",
        "bed",
        "bedroom",
        "bathroom",
        "check_in",
        "check_out",
        "house_type",
        "amenities",
        "facilities",
    )
    def get_object(self, queryset=None):
        house = super().get_object(queryset=queryset)
        if house.host.pk != self.request.user.pk:
            raise Http404()
        return house

class HousePhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.House
    template_name = "house/house_photos.html"
    def get_object(self, queryset=None):  
        house = super().get_object(queryset=queryset)
        if house.host.pk != self.request.user.pk:
            raise Http404()
        return house

class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    model = models.Photo
    template_name = "house/photo_create.html"
    fields = ("caption", "file")
    form_class = forms.CreatePhotoForm
    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo has been uploaded")
        return redirect(reverse("houses:photos", kwargs={"pk": pk}))

@login_required
def delete_photo(request, house_pk, photo_pk):
    user = request.user 
    try:
        house = models.House.objects.get(pk=house_pk)
        if house.host.pk != user.pk: 
            messages.error(request, "You don't have permission to delete this photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete() 
            messages.success(request, "Photo has been deleted") 
        return redirect(reverse("houses:photos", kwargs={"pk": house_pk}))
    except models.House.DoesNotExist: 
        return redirect(reverse("core:home"))
