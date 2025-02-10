class PokemonSearcher:

    @staticmethod
    def searchPokemonByName(nameQuery, cache):
        filters = {
            "query": nameQuery
        }
        
        return PokemonSearcher.searchPokemonWithMultipleFilters(cache, filters)[:5]

    @staticmethod
    def searchPokemonWithMultipleFilters(cache, filters):
        matches = []
        for data in cache.pokemonData.values():
            if filters["query"] not in data["name"]:
                continue

            if filters.get("vulnerable_to") and filters.get("vulnerable_to") not in data["vulnerable_to"]:
                continue
            
            if filters.get("super_effective") and filters.get("super_effective") not in data["super_effective"]:
                continue

            if filters.get("resistant_to") and filters.get("resistant_to") not in data["resistant_to"]:
                continue
            
            if filters.get("immune_to") and filters.get("immune_to") not in data["immune_to"]:
                continue

            if filters.get("pokedex_number") and int(filters.get("pokedex_number")) is not data["id"]:
                continue

            if filters.get("generation") and data["generation"] != filters["generation"]:
                continue

            if filters.get("types") and filters["types"] not in data["types"]:
                continue

            if filters.get("moves"):
                moves = filters.get("moves").split(',')
                if not all(move.strip() in data["moves"] for move in moves):
                    continue

            if filters.get("min_weight") and data["weight"] <= filters["min_weight"]:
                continue

            if filters.get("max_weight") and data["weight"] >= filters["max_weight"]:
                continue

            matches.append(data)

        return matches
