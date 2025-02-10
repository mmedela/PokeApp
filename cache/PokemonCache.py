import json

class PokemonCache:
    
    def __init__(self, cache_file, fetchPokemonListCallBack, fetchPokemonDataCallBack, fetchTypeEffectivenessCallBack):
        self.cacheFile = cache_file
        self.pokemonData = {}
        self.fetchPokemonListCallBack = fetchPokemonListCallBack
        self.fetchPokemonDataCallBack = fetchPokemonDataCallBack
        self.fetchTypeEffectivenessCallBack = fetchTypeEffectivenessCallBack

    def loadCache(self):
        try:
            with open(self.cacheFile, "r") as f:
                self.pokemonData = json.load(f)
            print("Cargado desde caché.")
            return True
        except FileNotFoundError:
            return False

    def saveCache(self):
        with open(self.cacheFile, "w") as f:
            json.dump(self.pokemonData, f, indent=4)
        print("Caché guardada correctamente.")

    def buildCache(self):
        print("Obteniendo lista de Pokémon...")
        pokemon_list = self.fetchPokemonListCallBack()

        print("Obteniendo datos de cada Pokémon...")
        self.pokemonData = {
            entry["name"]: self.fetchPokemonDataCallBack(entry["name"], entry["url"])
            for entry in pokemon_list
            if self.fetchPokemonDataCallBack(entry["name"], entry["url"])
        }

        print("Obteniendo efectividad de tipos...")
        type_effectiveness = self.fetchTypeEffectivenessCallBack()

        for data in self.pokemonData.values():
            data["vulnerable_to"] = list({
                eff for t in data["types"] for eff in type_effectiveness.get(t, {}).get("double_damage_from", [])
            })
            data["resistant_to"] = list({
                eff for t in data["types"] for eff in type_effectiveness.get(t, {}).get("half_damage_from", [])
            })
            data["immune_to"] = list({
                eff for t in data["types"] for eff in type_effectiveness.get(t, {}).get("no_damage_from", [])
            })
            data["super_effective"] = list({
                eff for t in data["types"] for eff in type_effectiveness.get(t, {}).get("double_damage_to", [])
            })

        self.saveCache()