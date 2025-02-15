import requests

from common import POKEMON_PROPERTY

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

class PokemonAPI:
    """Maneja la interacción con la PokeAPI."""
    
    @staticmethod
    def fetchPokemonList():
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon?limit=10000")
        return response.json()["results"] if response.status_code == 200 else []

    @staticmethod
    def fetchPokemonData(name, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        
        data = response.json()
        speciesData = requests.get(data["species"]["url"]).json()
        
        return {
            POKEMON_PROPERTY.POKEDEX_NUMBER.value: data["id"],
            POKEMON_PROPERTY.NAME.value: name,
            POKEMON_PROPERTY.GENERATION.value: speciesData["generation"]["name"],
            POKEMON_PROPERTY.HEIGHT.value: data["height"] * 10,
            POKEMON_PROPERTY.WEIGHT.value: data["weight"] / 10,
            POKEMON_PROPERTY.SPRITE.value: data['sprites']['front_default'],
            POKEMON_PROPERTY.TYPES.value: [t["type"]["name"] for t in data["types"]],
            POKEMON_PROPERTY.MOVES.value: [" ".join(move["move"]["name"].split("-")) for move in data["moves"]],
        }

    @staticmethod
    def fetchTypeEffectiveness():
        effectiveness = {}
        response = requests.get(f"{POKEAPI_BASE_URL}type?limit=100")
        if response.status_code != 200:
            return effectiveness
        
        for t in response.json()["results"]:
            typeData = requests.get(t["url"]).json()
            effectiveness[t["name"]] = {
                POKEMON_PROPERTY.VULNERABLE_TO.value: [damageType["name"] for damageType in typeData["damage_relations"]["double_damage_from"]],
                POKEMON_PROPERTY.RESISTANT_TO.value: [damageType["name"] for damageType in typeData["damage_relations"]["half_damage_from"]],
                POKEMON_PROPERTY.IMMUNE_TO.value: [damageType["name"] for damageType in typeData["damage_relations"]["no_damage_from"]],
                POKEMON_PROPERTY.SUPER_EFFECTIVE.value: [damageType["name"] for damageType in typeData["damage_relations"]["double_damage_to"]],
            }
        return effectiveness

