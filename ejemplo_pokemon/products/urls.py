from django.urls import path
from .views import pokemon_list, pokemon_details

urlpatterns = [
    path("", pokemon_list, name="pokemon_list"),  
    path('pokemon/<int:pokemon_id>/', pokemon_details, name="pokemons_datails"), 
]