import requests
import time
from products.models import Pokemon

def load_pokemons_to_db(offset=0, limit=100):
    """
    Carga Pokémon desde la API de PokeAPI a la base de datos en lotes de 100.
    """
    while True:
        url = f"https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit={limit}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data["results"]:  # 🔹 Si no hay más Pokémon, terminamos
                break

            pokemon_list = []

            for item in data["results"]:
                try:
                    details = requests.get(item["url"], timeout=10).json()
                    pokemon_id = details["id"]
                    image_url = details["sprites"]["front_default"] or "https://via.placeholder.com/150"
                    pokemon_type = ", ".join(t["type"]["name"].capitalize() for t in details["types"])
                    weight = details["weight"] / 10
                    height = details["height"] / 10
                    move = details["moves"][0]["move"]["name"].capitalize() if details["moves"] else "Desconocido"

                    # 🔹 Solo añadimos si no existe en la BD
                    if not Pokemon.objects.filter(pokemon_id=pokemon_id).exists():
                        pokemon_list.append(Pokemon(
                            pokemon_id=pokemon_id,
                            name=details["name"].capitalize(),
                            image=image_url,
                            type=pokemon_type,
                            weight=weight,
                            height=height,
                            move=move
                        ))

                    time.sleep(0.3)  # 🔹 Pequeño delay para evitar bloqueos

                except requests.RequestException as e:
                    print(f"❌ Error al obtener detalles de {item['name']}: {e}")

            # 🔹 Guardamos en la BD en una sola operación
            if pokemon_list:
                Pokemon.objects.bulk_create(pokemon_list)
                print(f"✔️ {len(pokemon_list)} Pokémon agregados (Offset: {offset}).")

            offset += limit  # 🔹 Avanzamos al siguiente lote de Pokémon

        except requests.RequestException as e:
            print(f"❌ Error al obtener la lista de Pokémon: {e}")
            break  # 🔹 Si hay error, salimos del bucle

    print("🎉 ¡Carga de Pokémon completada!")
def get_pokemons(offset=0, limit=100):
    """
    Obtiene una lista de Pokémon desde la base de datos.
    """
    return Pokemon.objects.all()[offset:offset+limit]
def get_pokemon_details(pokemon_id):
    """
    Obtiene los detalles de un Pokémon desde la base de datos.
    """
    try:
        pokemon = Pokemon.objects.get(pokemon_id=pokemon_id)
        return pokemon
    except Pokemon.DoesNotExist:
        return None