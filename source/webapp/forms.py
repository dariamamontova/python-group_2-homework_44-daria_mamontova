from django import forms
from webapp.models import Food


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = []