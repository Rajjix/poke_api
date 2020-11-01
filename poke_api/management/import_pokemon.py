import os
from typing import Callable

from poke_api.db.models import Pokemon
from poke_api.utils.csv_reader import CsvReader
from poke_api.utils.helpers import cast_primitive_type as cast_type
from poke_api.utils.modifiers import (
    PokemonModifier, BugFlyingTypeModifier, FireTypeModifier,
    InitialGInNameModifier, SteelTypeModifier)

from .csv_key_mappings import pokemon_property_mappings


def map_pokemon_properties(pokemon: dict) -> None:
    """
    Map pokemon properties from dict objects (based on valued from pokemon_property_mappings)
    also casts necesseray types.
    """
    for field, value in pokemon_property_mappings.items():
        pokemon[value["key"]] = cast_type(value["type"], pokemon.pop(field))


def is_valid_pokemon(pokemon: dict) -> bool:
    """
    Define a set a rules to filter which pokemon we want to import.
    """

    if pokemon.get("Legendary") == "True":
        return False

    if str(pokemon.get("Type 1", "")).lower() == "ghost":
        return False

    if str(pokemon.get("Type 2", "")).lower() == "ghost":
        return False

    return True


class ImportPokemon():
    """
    Allows importing new pokemon into out database, currently only supports csv.
    """

    @staticmethod
    def import_from_csv(args: 'argsparse.Namespace'):
        file_path = os.path.abspath(args.path)

        pokemons = CsvReader.read_csv_with_filter(
            path=file_path,
            custom_filter=is_valid_pokemon
        )

        for pokemon_props in pokemons:
            map_pokemon_properties(pokemon_props)

            pokemon = Pokemon(pokemon_props)

            # handle a chain of modifiers (precedence matters in case mofifiers adjust same attribute)
            pokemon_modifier = PokemonModifier(pokemon)
            pokemon_modifier.add_modifier(SteelTypeModifier(pokemon))
            pokemon_modifier.add_modifier(FireTypeModifier(pokemon))
            pokemon_modifier.add_modifier(BugFlyingTypeModifier(pokemon))
            pokemon_modifier.add_modifier(InitialGInNameModifier(pokemon))
            pokemon_modifier.handle()

            print("Name: ", pokemon.name.ljust(25, " "),
                  "Type: ", pokemon.type)
