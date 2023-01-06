from django.contrib import admin
from . import models 
from django.contrib.auth.admin import UserAdmin

@admin.register(models.User) 
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile", # Title
            {
                "fields": (
                    "avatar",
                    "gender",
                    "birthday",
                    "language",
                    "superhost",
                    "bio",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    list_filter = UserAdmin.list_filter
    pass

# admin.site.register(models.User, CustomUserAdmin)