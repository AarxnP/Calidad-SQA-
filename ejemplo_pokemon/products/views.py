from django.shortcuts import render
from .services.product_service import get_pokemons, get_pokemon_details

def pokemon_list(request):
    limit = 20  # Define el límite de pokemons por página
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * limit
    pokemons = get_pokemons(offset=offset, limit=limit)
    total_pages = (1304 + limit - 1) // limit  # Calcula el número total de páginas
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
    # Arreglo del error tipográfico en el nombre de la vista
    pokemon = get_pokemon_details(pokemon_id)
    if not pokemon:
        return render(request, "404.html", status=404)  # Página de error si no encuentra el Pokémon
    return render(request, "pokemons_datails.html", {"pokemon": pokemon})
