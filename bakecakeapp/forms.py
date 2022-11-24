from django import forms

from .models import Ingredient


class CreateCakeForm(forms.Form):
    levels = forms.ModelChoiceField(
        label='Уровни',
        queryset=Ingredient.objects.filter(type='LV'),
        widget=forms.RadioSelect(attrs={'v-model': 'Levels'}))
    shape = forms.ModelChoiceField(
        label='Форма',
        queryset=Ingredient.objects.filter(type='SH'),
        widget=forms.RadioSelect(attrs={'v-model': 'Form'}))
    topping = forms.ModelChoiceField(
        label='Топпинг',
        queryset=Ingredient.objects.filter(type='TP'),
        widget=forms.RadioSelect(attrs={'v-model': 'Topping'}))
    berries = forms.ModelChoiceField(
        label='Ягоды',
        queryset=Ingredient.objects.filter(type='BR'),
        widget=forms.RadioSelect(attrs={'v-model': 'Berries'}))
    decor = forms.ModelChoiceField(
        label='Декор',
        queryset=Ingredient.objects.filter(type='DC'),
        widget=forms.RadioSelect(attrs={'v-model': 'Decor'}))
    writing = forms.CharField(max_length=255)
