from django.shortcuts import render, get_object_or_404, redirect
from .services.product_service import get_pokemons, get_pokemon_details, create_pokemon, update_pokemon, delete_pokemon
from .form import PokemonForm

def pokemon_list(request):
    limit = 20  # Define el límite de pokemons por página
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * limit

    pokemons = get_pokemons(offset=offset, limit=limit)

    # Filtrar solo los Pokémon con información válida
    pokemons = [p for p in pokemons if hasattr(p, "name") and hasattr(p, "id")]

    total_pokemons = 1304 + len(get_pokemons(offset=1304, limit=100))  # Contar nuevos Pokémon
    total_pages = (total_pokemons + limit - 1) // limit

    previous_page = page - 1 if page > 1 else 1
    next_page = page + 1 if page < total_pages else total_pages

    return render(request, "pokemon_list.html", {
        "pokemons": pokemons,
        "next_url": next_page,
        "prev_url": previous_page,
        "offset": offset,
        "limit": limit,
        "current_page": page,
        "total_pages": total_pages,
    })  

def pokemon_details(request, pokemon_id):
    pokemon = get_pokemon_details(pokemon_id)
    if not pokemon or not hasattr(pokemon, "name"):
        return render(request, "404.html", status=404)  
    return render(request, "pokemons_datails.html", {"pokemon": pokemon})

# CREAR POKÉMON
def pokemon_create(request):
    if request.method == "POST":
        form = PokemonForm(request.POST)
        if form.is_valid():
            new_pokemon = create_pokemon(form.cleaned_data)  # Crea el Pokémon
            return redirect("pokemon_details", pokemon_id=new_pokemon.id)
    else:
        form = PokemonForm()
    return render(request, "pokemon_form.html", {"form": form})

# EDITAR POKÉMON
def pokemon_edit(request, pokemon_id):
    pokemon = get_pokemon_details(pokemon_id)
    if not pokemon or not hasattr(pokemon, "name"):
        return render(request, "404.html", status=404)  

    if request.method == "POST":
        form = PokemonForm(request.POST, instance=pokemon)
        if form.is_valid():
            update_pokemon(pokemon_id, form.cleaned_data)  # Actualiza datos
            return redirect("pokemons_datails", pokemon_id=pokemon_id)
    else:
        form = PokemonForm(instance=pokemon)

    return render(request, "pokemon_form.html", {"form": form})

# ELIMINAR POKÉMON
def pokemon_delete(request, pokemon_id):
    if request.method == "POST":
        delete_pokemon(pokemon_id)  # Llama al servicio para eliminar
        return redirect("pokemon_list")

    return render(request, "pokemon_confirm_delete.html", {"pokemon_id": pokemon_id})
