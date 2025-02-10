import requests

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
            "id": data["id"],
            "name": name,
            "generation": speciesData["generation"]["name"],
            "height": data["height"] * 10,
            "weight": data["weight"] / 10,
            "sprite": data['sprites']['front_default'],
            "types": [t["type"]["name"] for t in data["types"]],
            "moves": [" ".join(move["move"]["name"].split("-")) for move in data["moves"]],
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
                "double_damage_from": [damageType["name"] for damageType in typeData["damage_relations"]["double_damage_from"]],
                "half_damage_from": [damageType["name"] for damageType in typeData["damage_relations"]["half_damage_from"]],
                "no_damage_from": [damageType["name"] for damageType in typeData["damage_relations"]["no_damage_from"]],
                "double_damage_to": [damageType["name"] for damageType in typeData["damage_relations"]["double_damage_to"]],
                "half_damage_to": [damageType["name"] for damageType in typeData["damage_relations"]["half_damage_to"]],
                "no_damage_to": [damageType["name"] for damageType in typeData["damage_relations"]["no_damage_to"]]
            }
        return effectiveness

