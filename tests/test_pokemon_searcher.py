import pytest
from unittest.mock import MagicMock
from filter.PokemonSearcher import PokemonSearcher 

@pytest.fixture
def mockCache():
    mockCache = MagicMock()
    mockCache.pokemonData = {
        "pikachu": {
            "name": "pikachu",
            "generation": "generation-i",
            "types": ["electric"],
            "weight": 6,
            "moves": ["quick-attack", "thunderbolt"]
        },
        "bulbasaur": {
            "name": "bulbasaur",
            "generation": "generation-i",
            "types": ["grass", "poison"],
            "weight": 7,
            "moves": ["tackle", "vine-whip"]
        },
        "charizard": {
            "name": "charizard",
            "generation": "generation-i",
            "types": ["fire", "flying"],
            "weight": 90,
            "moves": ["flamethrower", "fly"]
        },
        "blastoise": {
            "name": "blastoise",
            "generation": "generation-i",
            "types": ["water"],
            "weight": 85,
            "moves": ["water-gun", "hydro-pump"]
        }
    }
    return mockCache


def testSearchPokemonByName(mockCache):
    name_query = "pikachu"
    result = PokemonSearcher.searchPokemonByName(name_query, mockCache)
    
    assert len(result) == 1
    assert result[0]["name"] == "pikachu"


def testSearchPokemonWithMultipleFilters(mockCache):
    filters = {
        "query": "saur",  
        "generation": "generation-i",
        "types": "grass",  
        "min_weight": 5,   
        "max_weight": 10   
    }
    result = PokemonSearcher.searchPokemonWithMultipleFilters(mockCache, filters)
    
    assert len(result) == 1
    assert result[0]["name"] == "bulbasaur"


def testSearchPokemonWithMovesFilter(mockCache):
    filters = {
        "query": "charizard",
        "moves": "flamethrower,fly" 
    }
    result = PokemonSearcher.searchPokemonWithMultipleFilters(mockCache, filters)
    
    assert len(result) == 1
    assert result[0]["name"] == "charizard"


def testSearchPokemonWithWeightFilter(mockCache):
    filters = {
        "query": "charizard",
        "min_weight": 80, 
        "max_weight": 100  
    }
    result = PokemonSearcher.searchPokemonWithMultipleFilters(mockCache, filters)
    
    assert len(result) == 1
    assert result[0]["name"] == "charizard"


def testSearchPokemonWithNoMatches(mockCache):
    filters = {
        "query": "pikachu",
        "types": "fire", 
    }
    result = PokemonSearcher.searchPokemonWithMultipleFilters(mockCache, filters)
    
    assert len(result) == 0
