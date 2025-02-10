from flask import Flask, render_template, request
import os
from HtmlTags.createComponents import createDropDownSearchOptions, createPaginationControllers, createPartialNameQueryButton
from api.PokemonApi import PokemonAPI
from cache.PokemonCache import PokemonCache
from filter.PokemonSearcher import PokemonSearcher

app = Flask(__name__)

CACHE_DIR = "cache"
POKEMON_CACHE_FILE = os.path.join(CACHE_DIR, "pokemon_data.json")
LIST_OF_TYPES = [   "Any",
                    "Fire",
                    "Water",
                    "Grass",
                    "Electric",
                    "Ice",
                    "Fighting",
                    "Poison",
                    "Ground",
                    "Flying",
                    "Psychic",
                    "Bug",
                    "Rock",
                    "Ghost",
                    "Dragon",
                    "Dark",
                    "Steel",
                    "Fairy",]

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
        "query": request.args.get("name", "").lower(),
        "vulnerable_to": request.args.get("vulnerable-to", "").lower(),
        "super_effective": request.args.get("super-effective", "").lower(),
        "resistant_to": request.args.get("resistant-to", "").lower(),
        "immune_to": request.args.get("immune-to", "").lower(),
        "pokedex_number": request.args.get("pokedex-number", "").lower(),
        "types": request.args.get("types", "").lower(),
        "generation": request.args.get("generation", "").lower(),
        "moves": request.args.get("move"),
        "min_weight": float(request.args.get("min-weight", 0) or 0),
        "max_weight": float(request.args.get("max-weight", 0) or 0)
    }
    matches = PokemonSearcher.searchPokemonWithMultipleFilters(cache, filters)

    page = int(request.args.get("page", 1))
    limit = 6
    totalPages = (len(matches) + limit - 1) // limit
    start, end = (page - 1) * limit, page * limit
    paginatedResults = matches[start:end]
    resultsHtml = render_template("pokemon_info.html", pokemon_list=paginatedResults)

    paginationHtml = createPaginationControllers(page, totalPages, filters["query"]) if totalPages > 1 else ""

    return resultsHtml + paginationHtml


@app.route("/pokemon/<name>")
def get_pokemon(name):
    pokemon = cache.pokemonData.get(name.lower())
    print(pokemon)
    return render_template("pokemon_info.html", pokemon_list=[pokemon]) if pokemon else "<p class='text-red-500'>Pokémon not found</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

