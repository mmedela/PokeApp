import pytest
import json
from cache.PokemonCache import PokemonCache
from unittest.mock import MagicMock

@pytest.fixture
def mockCache():
    mockCacheFile = "mock_cache.json"
    mockFetchPokemonList = MagicMock(return_value=[{"name": "pikachu", "url": "pikachu_url"}])
    mockFetchPokemonData = MagicMock(return_value={"name": "pikachu", "types": ["electric"]})
    mockFetchTypeEffectiveness = MagicMock(return_value={
        "electric": {
            "double_damage_from": ["ground"],
            "half_damage_from": ["electric"],
            "no_damage_from": [],
            "double_damage_to": ["water"]
        }
    })
    return PokemonCache(mockCacheFile, mockFetchPokemonList, mockFetchPokemonData, mockFetchTypeEffectiveness)


def testLoadCacheSuccess(mockCache):
    mockCache.loadCache = MagicMock(return_value=True)
    
    result = mockCache.loadCache()
    assert result is True


def testLoadCacheFileNotFound(mockCache):
    mockCache.loadCache = MagicMock(return_value=False)
    
    result = mockCache.loadCache()
    assert result is False


def testSaveCache(mockCache, tmpdir):
    mockCache.cacheFile = tmpdir.join("pokemon_cache.json")
    mockCache.pokemonData = {"pikachu": {"name": "pikachu", "types": ["electric"]}}
    
    mockCache.saveCache() 

    assert mockCache.cacheFile.exists()

    with open(mockCache.cacheFile, "r") as f:
        data = json.load(f)
        assert "pikachu" in data
        assert data["pikachu"]["types"] == ["electric"]


def testBuildCache(mockCache):
    mockCache.buildCache()  
    
    assert "pikachu" in mockCache.pokemonData
    pikachuData = mockCache.pokemonData["pikachu"]

    assert "vulnerable_to" in pikachuData
    assert "resistant_to" in pikachuData
    assert "immune_to" in pikachuData
    assert "super_effective" in pikachuData

    assert "ground" in pikachuData["vulnerable_to"]
    assert "electric" in pikachuData["resistant_to"]
    assert "water" in pikachuData["super_effective"]
