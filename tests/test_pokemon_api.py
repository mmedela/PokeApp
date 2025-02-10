import pytest
from unittest.mock import patch, MagicMock
from api.PokemonApi import PokemonAPI

@patch('api.PokemonApi.requests.get')
def testFetchPokemonListSuccess(mock_get):
    mockResponse = MagicMock()
    mockResponse.status_code = 200
    mockResponse.json.return_value = {"results": [{"name": "pikachu", "url": "url1"}]}
    mock_get.return_value = mockResponse
    
    result = PokemonAPI.fetchPokemonList()
    
    assert len(result) == 1
    assert result[0]["name"] == "pikachu"


@patch('api.PokemonApi.requests.get')
def testFetchPokemonListFailure(mock_get):
    mockResponse = MagicMock()
    mockResponse.status_code = 404
    mock_get.return_value = mockResponse
    
    result = PokemonAPI.fetchPokemonList()
    
    assert result == []


# Test for fetchPokemonData
@patch('api.PokemonApi.requests.get')
def testFetchPokemonDataSuccess(mock_get):
    mockPokemonResponse = MagicMock()
    mockPokemonResponse.status_code = 200
    mockPokemonResponse.json.return_value = {
        "id": 1,
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "sprites": {"front_default": "pikachu_sprite_url"},
        "types": [{"type": {"name": "electric"}}],
        "moves": [{"move": {"name": "thunderbolt"}}],
        "species": {"url": "species_url"}
    }
    
    mockSpeciesResponse = MagicMock()
    mockSpeciesResponse.status_code = 200
    mockSpeciesResponse.json.return_value = {
        "generation": {"name": "generation-1"}
    }

    mock_get.side_effect = [mockPokemonResponse, mockSpeciesResponse]

    result = PokemonAPI.fetchPokemonData("pikachu", "pokemon_url")
    
    assert result["name"] == "pikachu"
    assert result["generation"] == "generation-1"
    assert result["types"] == ["electric"]
    assert result["moves"] == ["thunderbolt"]


@patch('api.PokemonApi.requests.get')
def testFetchPokemonDataFailure(mock_get):
    mockResponse = MagicMock()
    mockResponse.status_code = 404
    mock_get.return_value = mockResponse
    
    result = PokemonAPI.fetchPokemonData("pikachu", "pokemon_url")
    
    assert result is None


@patch('api.PokemonApi.requests.get')
def testFetchTypeEffectivenessSuccess(mock_get):
    mockResponse = MagicMock()
    mockResponse.status_code = 200
    mockResponse.json.return_value = {
        "results": [{"name": "electric", "url": "url1"}] 
    }

    mockTypeDataResponse = MagicMock()
    mockTypeDataResponse.status_code = 200
    mockTypeDataResponse.json.return_value = {
        "damage_relations": {
            "double_damage_from": [{"name": "ground"}],
            "half_damage_from": [{"name": "electric"}],
            "no_damage_from": [],
            "double_damage_to": [{"name": "water"}],
            "half_damage_to": [],
            "no_damage_to": []
        }
    }
    
    
    mock_get.side_effect = [mockResponse, mockTypeDataResponse]

    result = PokemonAPI.fetchTypeEffectiveness()

   
    assert "electric" in result  
    assert "double_damage_from" in result["electric"]  
    assert "ground" in result["electric"]["double_damage_from"] 
    assert "water" in result["electric"]["double_damage_to"]  


@patch('api.PokemonApi.requests.get')
def testFetchTypeEffectivenessFailure(mock_get):
    mockResponse = MagicMock()
    mockResponse.status_code = 404
    mock_get.return_value = mockResponse
    
    result = PokemonAPI.fetchTypeEffectiveness()
    
    assert result == {}


