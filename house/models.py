from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django_countries.fields import CountryField
from django.urls import reverse
from cal import Calendar
from core import models as core_models

# Create your models here.
class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    class Meta:
        abstract = True

class Photo(core_models.TimeStampedModel):
    caption = models.CharField(max_length=80)
    file = models.ImageField()
    house = models.ForeignKey("House", related_name="photo", on_delete=models.CASCADE)

class AbstractItem(core_models.TimeStampedModel):
    # Define abstract object
    name = models.CharField(max_length=150)
    class Meta:
        abstract = True
    def __str__(self) -> str:
        return self.name

class Amenity(AbstractItem):
    class Meta:
        verbose_name_plural = "Amenities"

class HouseType(AbstractItem):
    class Meta:
        verbose_name = "House type"

class Facility(AbstractItem):
    class Meta:
        verbose_name_plural = "Facilities"

class Photo(core_models.TimeStampedModel):
    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="house_photos",)
    house = models.ForeignKey("House", related_name="photos", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.caption

class House(models.Model):
    # id = models.IntegerField()
    name = models.TextField(max_length=100)
    description = models.TextField()

    country = CountryField()
    city = models.CharField(max_length=30)

    price = models.IntegerField(default=0)

    address = models.TextField(max_length=100, default='abc')

    guest = models.IntegerField(default=0)
    bedroom = models.IntegerField(default=0)
    bed = models.IntegerField(default=0)
    bathroom = models.IntegerField(default=0)

    check_in = models.TimeField(null=True)
    check_out = models.TimeField(null=True)

    host = models.ForeignKey("users.User", related_name="houses", on_delete=models.CASCADE, null=True)
    house_type =models.ForeignKey("HouseType", verbose_name="House type", related_name="houses", on_delete=models.CASCADE, null=True, blank=True)

    amenities = models.ManyToManyField("Amenity", related_name="houses", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="houses", blank=True)        

    def __str__(self):
        return self.name

    def amenities_count(self):
        # return "\n".join([ame.amenity for ame in self.amenities.all()])
        return self.amenities.count()
    amenities_count.short_description = "amenity"

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None
    
    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_rating = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_rating += review.avgRating()
            return round(all_rating/len(all_reviews), 2)
        return 0
    total_rating.short_description = "rating"

    def truncated_description(self):
        return Truncator(self.description).words(10, truncate='...')

    def save_city(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save_city(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("houses: detail", kwargs={"pk": self.pk})
    


