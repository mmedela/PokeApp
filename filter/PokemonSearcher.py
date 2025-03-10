from common import POKEMON_PROPERTY


class PokemonSearcher:

    @staticmethod
    def searchPokemonByName(nameQuery, cache):
        filters = {
            POKEMON_PROPERTY.NAME: nameQuery
        }
        
        return PokemonSearcher.searchPokemonWithMultipleFilters(cache, filters)[:5]

    @staticmethod
    def searchPokemonWithMultipleFilters(cache, filters):
        matches = []
        for data in cache.pokemonData.values():
            if filters.get(POKEMON_PROPERTY.NAME) not in data[POKEMON_PROPERTY.NAME.value]:
                continue

            if filters.get(POKEMON_PROPERTY.VULNERABLE_TO) and filters[POKEMON_PROPERTY.VULNERABLE_TO] not in data[POKEMON_PROPERTY.VULNERABLE_TO.value]:
                continue
            
            if filters.get(POKEMON_PROPERTY.SUPER_EFFECTIVE) and filters[POKEMON_PROPERTY.SUPER_EFFECTIVE] not in data[POKEMON_PROPERTY.SUPER_EFFECTIVE.value]:
                continue

            if filters.get(POKEMON_PROPERTY.RESISTANT_TO) and filters[POKEMON_PROPERTY.RESISTANT_TO] not in data[POKEMON_PROPERTY.RESISTANT_TO.value]:
                continue
            
            if filters.get(POKEMON_PROPERTY.IMMUNE_TO) and filters[POKEMON_PROPERTY.IMMUNE_TO] not in data[POKEMON_PROPERTY.IMMUNE_TO.value]:
                continue

            if filters.get(POKEMON_PROPERTY.POKEDEX_NUMBER) and int(filters[POKEMON_PROPERTY.POKEDEX_NUMBER]) is not data[POKEMON_PROPERTY.POKEDEX_NUMBER.value]:
                continue

            if filters.get(POKEMON_PROPERTY.GENERATION) and data[POKEMON_PROPERTY.GENERATION.value] != filters[POKEMON_PROPERTY.GENERATION]:
                continue

            if filters.get(POKEMON_PROPERTY.TYPES) and filters[POKEMON_PROPERTY.TYPES] not in data[POKEMON_PROPERTY.TYPES.value]:
                continue

            if filters.get(POKEMON_PROPERTY.MOVES):
                moves = filters[POKEMON_PROPERTY.MOVES].split(',')
                if not all(move.strip() in data[POKEMON_PROPERTY.MOVES.value] for move in moves):
                    continue

            if filters.get(POKEMON_PROPERTY.MIN_WEIGHT) and data[POKEMON_PROPERTY.WEIGHT.value] <= filters[POKEMON_PROPERTY.MIN_WEIGHT]:
                continue

            if filters.get(POKEMON_PROPERTY.MAX_WEIGHT) and data[POKEMON_PROPERTY.WEIGHT.value] >= filters[POKEMON_PROPERTY.MAX_WEIGHT]:
                continue

            matches.append(data)

        return matches
