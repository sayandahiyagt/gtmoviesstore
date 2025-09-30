from django import forms
from .models import Petition


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ["title", "description", "rationale"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Movie title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Brief description of the movie"}),
            "rationale": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Why should this be included?"}),
        }