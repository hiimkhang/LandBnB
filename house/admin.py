from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
@admin.register(models.HouseType)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.houses.count()

@admin.register(models.Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Facility)
class FacilityAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_thumbnail",)
    
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"

class PhotoInline(admin.TabularInline):
    model = models.Photo
@admin.register(models.House)
class HouseAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                )
            },
        ),
        (
            "Times",
            {
                "fields": (
                    "check_in",
                    "check_out",
                )
            },
        ),
        (
            "Spaces",
            {
                "fields": (
                    "guest",
                    "bed",
                    "bedroom",
                    "bathroom",
                )
            },
        ),
        (
            "More About the Space",
            {
                "fields": (
                    "amenities",
                    "facilities",
                )
            },
        ),
        (
            "Last Details",
            {"fields": ("host",)},
        ),
    )

    ordering = (
        "name",
        "price",
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guest",
        "bedroom",
        "bed",
        "bathroom",
        "check_in",
        "check_out",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "house_type",
        "amenities",
        "facilities",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = (
        "city",
        "^host__username",
        "^name",
    )

    filter_horizontal = (
        "amenities",
        "facilities",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenity Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"