from django import forms
from .models import Pokemon

class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['name', 'pokemon_id', 'image', 'type', 'weight', 'height', 'move']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'pokemon_id': forms.NumberInput(attrs={"class": "form-control"}),
            'image': forms.URLInput(attrs={"class": "form-control"}),
            'type': forms.TextInput(attrs={"class": "form-control"}),
            'weight': forms.NumberInput(attrs={"class": "form-control"}),
            'height': forms.NumberInput(attrs={"class": "form-control"}),
            'move': forms.TextInput(attrs={"class": "form-control"})
        }