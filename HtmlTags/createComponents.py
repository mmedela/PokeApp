from HtmlTags.HtmlTag import HtmlTag

def createDropDownSearchOptions(pokemonName):
    button = HtmlTag("button", {
        "class": "block w-full text-left p-2 bg-gray-200 hover:bg-gray-300 rounded mt-1",
        "hx-get": f"/pokemon/{pokemonName}",
        "hx-target": "#search-results-container",
        "hx-include": "[name=generation], [name=attack-type], [name=move]",
        "onclick": "hideResultsOnSelect()"
    }, [pokemonName.capitalize()])

    return button.render()
    

def createDropDownSearchOptions(pokemonName):
    button = HtmlTag("button", {
        "class": "block w-full text-left p-2 bg-gray-200 hover:bg-gray-300 rounded mt-1",
        "hx-get": f"/pokemon/{pokemonName}",
        "hx-target": "#search-results-container",
        "hx-include": "[name=generation], [name=attack-type], [name=move]",
        "onclick": "hideResultsOnSelect()"
    }, [pokemonName.capitalize()])

    return button.render()

def createPartialNameQueryButton(pokemonName):

    button = HtmlTag("button", {
        "class": "block w-full p-2 bg-blue-500 text-white rounded mt-1",
        "hx-get":f"/search-results?name={pokemonName}",
        "hx-target": "#search-results-container",
        "hx-trigger":"click",
        "hx-include": "[name=generation], [name=attack-type], [name=move]",
        "onclick": "hideResultsOnSelect()"
    }, ["See All Results"])

    return button.render()

def createPaginationControllers(page, totalPages):
    div = HtmlTag('div', {
        "class": "flex justify-between mt-2"
    })
    prevButton = HtmlTag("button", {
        "hx-get":f'/search-results?page={page-1}',
        "hx-target":'#search-results-container',
        "class":'px-3 py-1 bg-gray-300 hover:bg-gray-400 rounded',
        "hx-include":"[name=generation],\
                            [name=move],\
                            [name=region],\
                            [name=min_weight],\
                            [name=max_weight],\
                            [name=vulnerable_to],\
                            [name=super_effective],\
                            [name=resistant_to],\
                            [name=immune_to],\
                            [name=types], \
                            [name=pokedex-number],\
                            [name=name]"
    }, ["Prev"])
    if page == 1:
        prevButton.addAttribute("disabled", "true")

    pageCounter = HtmlTag('span', {}, [f"Page {page} of {totalPages}"])

    nextButton = HtmlTag("button", {
        "hx-get":f'/search-results?page={page+1}',
        "hx-target":'#search-results-container',
        "class":'px-3 py-1 bg-gray-300 hover:bg-gray-400 rounded',
        "hx-include":"[name=generation],\
                            [name=move],\
                            [name=region],\
                            [name=min_weight],\
                            [name=max_weight],\
                            [name=vulnerable_to],\
                            [name=super_effective],\
                            [name=resistant_to],\
                            [name=immune_to],\
                            [name=types], \
                            [name=pokedex-number],\
                            [name=name]"
    }, ["Next"])
    if page == totalPages:
        nextButton.addAttribute("disabled", "true")

    div.addChild(prevButton)
    div.addChild(pageCounter)
    div.addChild(nextButton)

    return div.render()