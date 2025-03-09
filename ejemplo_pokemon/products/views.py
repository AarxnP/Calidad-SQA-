from django.shortcuts import render
from .services.product_service import get_pokemons, get_pokemon_detail

def pokemon_list(request):
    offset = int(request.GET.get('offset', 0))
    limit = 10  # Límite de 10 Pokémon por página

    # Llamar al servicio para obtener los Pokémon con paginación
    pokemons, next_url, prev_url = get_pokemons(offset=offset, limit=limit)

    # Calcular la página actual
    current_page = offset // limit + 1

    # Pasar las URLs previas y siguientes con el offset adecuado
    prev_offset = offset - limit if offset > 0 else None
    next_offset = offset + limit if next_url else None

    return render(request, "pokemon_list.html", {
        "pokemons": pokemons,
        "next_url": next_url,
        "prev_url": prev_url,
        "offset": offset,
        "limit": limit,
        "current_page": current_page,
        "prev_offset": prev_offset,
        "next_offset": next_offset
    })


def pokemon_details(request, pokemon_id):
    # Arreglo del error tipográfico en el nombre de la vista
    pokemon = get_pokemon_detail(pokemon_id)
    if not pokemon:
        return render(request, "404.html", status=404)  # Página de error si no encuentra el Pokémon
    return render(request, "pokemons_datails.html", {"pokemon": pokemon})
