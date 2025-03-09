import requests

def get_pokemons(offset=0, limit=10):
    url = f"https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit={limit}"  # Usar offset y limit para paginación
    try:
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json()
        pokemons = []

        for item in datos["results"]:
            try:
                # Obtenemos los detalles de cada Pokémon
                detalles = requests.get(item["url"], timeout=5).json()
                image_url = detalles["sprites"]["front_default"]

                pokemon = {
                    "id": detalles["id"],
                    "name": detalles["name"].capitalize(),
                    "image": image_url if image_url else "https://via.placeholder.com/150",
                    "type": ", ".join(t["type"]["name"].capitalize() for t in detalles["types"]),
                    "weight": detalles["weight"] / 10,  # Peso en kg
                    "height": detalles["height"] / 10,  # Altura en metros
                    "move": detalles["moves"][0]["move"]["name"].capitalize() if detalles["moves"] else "Desconocido",
                }
                pokemons.append(pokemon)

            except requests.RequestException as e:
                print(f"Error al obtener detalles de {item['name']}: {e}")

        # Devolver la lista de Pokémon, junto con los enlaces de la página siguiente y anterior
        return pokemons, datos.get("next"), datos.get("previous")

    except requests.RequestException as e:
        print(f"Error al obtener la lista de Pokémon: {e}")
        return [], None, None  # Si hay un error, devolver una lista vacía y sin enlaces

def get_pokemon_detail(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    try:
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()
        detalles = respuesta.json()

        return {
            "id": detalles["id"],
            "name": detalles["name"].capitalize(),
            "image": detalles["sprites"]["front_default"] if detalles["sprites"]["front_default"] else "https://via.placeholder.com/150",
            "type": ", ".join(t["type"]["name"].capitalize() for t in detalles["types"]),
            "weight": detalles["weight"] / 10,
            "height": detalles["height"] / 10,
            "move": detalles["moves"][0]["move"]["name"].capitalize() if detalles["moves"] else "Desconocido",
        }

    except requests.RequestException as e:
        print(f"Error al obtener detalles del Pokémon con ID {pokemon_id}: {e}")
        return None  # Devuelve None si hay un error
