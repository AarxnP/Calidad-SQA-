from django.urls import path
from .views import pokemon_list, pokemon_details, pokemon_create, pokemon_edit, pokemon_delete

urlpatterns = [
    path('', pokemon_list, name="pokemon_list"),
    path('<int:pokemon_id>/', pokemon_details, name="pokemons_datails"),
    path('create/', pokemon_create, name="pokemon_create"),
    path('<int:pokemon_id>/edit/', pokemon_edit, name="edit_pokemon"),
    path('<int:pokemon_id>/delete/', pokemon_delete, name="delete_pokemon"),
]
