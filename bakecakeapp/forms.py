from django import forms

from .models import Ingredient


class CreateCakeForm(forms.Form):
    #levels
    #shape
    topping = forms.ModelChoiceField(
        label='Топпинг',
        queryset=Ingredient.objects.filter(type='TP'),
        widget=forms.RadioSelect)
    berries = forms.ModelChoiceField(
        label='Ягоды',
        queryset=Ingredient.objects.filter(type='BR'),
        widget=forms.RadioSelect)
    decor = forms.ModelChoiceField(
        label='Декор',
        queryset=Ingredient.objects.filter(type='DC'),
        widget=forms.RadioSelect)
    writing = forms.CharField(max_length=255)
