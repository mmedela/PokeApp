from common import POKEMON_PROPERTY, LIST_OF_TYPES
from flask import Flask, render_template, request
import os
from HtmlTags.createComponents import createDropDownSearchOptions, createPaginationControllers, createPartialNameQueryButton
from api.PokemonApi import PokemonAPI
from cache.PokemonCache import PokemonCache
from filter.PokemonSearcher import PokemonSearcher

app = Flask(__name__)

CACHE_DIR = "cache"
POKEMON_CACHE_FILE = os.path.join(CACHE_DIR, "pokemon_data.json")


cache = PokemonCache(
    POKEMON_CACHE_FILE, 
    PokemonAPI.fetchPokemonList, 
    PokemonAPI.fetchPokemonData,
    PokemonAPI.fetchTypeEffectiveness
)
if not cache.loadCache():
    cache.buildCache()


@app.route("/")
def index():
    return render_template("index.html", type_list=LIST_OF_TYPES)


@app.route("/search-dropdown", methods=["GET"])
def search_dropdown():
    query = request.args.get("name", "").lower()
    matches = PokemonSearcher.searchPokemonByName(query, cache)

    results = [ createDropDownSearchOptions(pokemon["name"]) for pokemon in matches]

    if results:
        results.append(createPartialNameQueryButton(query))

    return "".join(results)


@app.route("/search-results", methods=["GET"])
def search_results():
    filters = {
        POKEMON_PROPERTY.NAME: request.args.get(POKEMON_PROPERTY.NAME.value, "").lower(),
        POKEMON_PROPERTY.VULNERABLE_TO: request.args.get(POKEMON_PROPERTY.VULNERABLE_TO.value, "").lower(),
        POKEMON_PROPERTY.SUPER_EFFECTIVE: request.args.get(POKEMON_PROPERTY.SUPER_EFFECTIVE.value, "").lower(),
        POKEMON_PROPERTY.RESISTANT_TO: request.args.get(POKEMON_PROPERTY.RESISTANT_TO.value, "").lower(),
        POKEMON_PROPERTY.IMMUNE_TO: request.args.get(POKEMON_PROPERTY.IMMUNE_TO.value, "").lower(),
        POKEMON_PROPERTY.POKEDEX_NUMBER: request.args.get(POKEMON_PROPERTY.POKEDEX_NUMBER.value, "").lower(),
        POKEMON_PROPERTY.TYPES: request.args.get(POKEMON_PROPERTY.TYPES.value, "").lower(),
        POKEMON_PROPERTY.GENERATION: request.args.get(POKEMON_PROPERTY.GENERATION.value, "").lower(),
        POKEMON_PROPERTY.MOVES: request.args.get(POKEMON_PROPERTY.MOVES.value),
        POKEMON_PROPERTY.MIN_WEIGHT: float(request.args.get(POKEMON_PROPERTY.MIN_WEIGHT.value, 0) or 0),
        POKEMON_PROPERTY.MAX_WEIGHT: float(request.args.get(POKEMON_PROPERTY.MAX_WEIGHT.value, 0) or 0)
    }
    matches = PokemonSearcher.searchPokemonWithMultipleFilters(cache, filters)

    page = int(request.args.get("page", 1))
    limit = 6
    totalPages = (len(matches) + limit - 1) // limit
    start, end = (page - 1) * limit, page * limit
    paginatedResults = matches[start:end]
    resultsHtml = render_template("pokemon_info.html", pokemon_list=paginatedResults)

    paginationHtml = createPaginationControllers(page, totalPages) if totalPages > 1 else ""

    return resultsHtml + paginationHtml


@app.route("/pokemon/<name>")
def get_pokemon(name):
    pokemon = cache.pokemonData.get(name.lower())
    return render_template("pokemon_info.html", pokemon_list=[pokemon]) if pokemon else "<p class='text-red-500'>Pokémon not found</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

