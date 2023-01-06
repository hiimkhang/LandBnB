from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    customer_service = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    suitable_price = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "customer_service",
            "cleanliness",
            "location",
            "suitable_price",
        )

    def save(self):
        review = super().save(commit=False)
        return review