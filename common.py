from enum import Enum

class POKEMON_PROPERTY(Enum):
    NAME = "name"
    VULNERABLE_TO = "vulnerable_to"
    SUPER_EFFECTIVE = "super_effective"
    RESISTANT_TO = "resistant_to"
    IMMUNE_TO = "immune_to"
    POKEDEX_NUMBER = "id"
    TYPES = "types"
    GENERATION = "generation"
    MOVES = "moves"
    MIN_WEIGHT = "min_weight"
    MAX_WEIGHT = "max_weight"
    SPRITE = "sprite"
    HEIGHT = "height"
    WEIGHT = "weight"
    
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