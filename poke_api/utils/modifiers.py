

class PokemonModifier:
    def __init__(self, pokemon: 'Pokemon'):
        self.pokemon = pokemon
        self.next_modifier = None

    def add_modifier(self, modifier: 'PokemonModifier'):
        if self.next_modifier:
            self.next_modifier.add_modifier(modifier)
        else:
            self.next_modifier = modifier

    def handle(self):
        if self.next_modifier:
            self.next_modifier.handle()


class SteelTypeModifier(PokemonModifier):
    """
    Double HP for Steel type pokemon
    """

    def handle(self):
        if "Steel" in self.pokemon.type:
            # print(f"Doubling {self.pokemon.name}'s hp")
            self.pokemon.hp *= 2
        super().handle()


class FireTypeModifier(PokemonModifier):
    """
    Decrease attack by 10% for Fire type pokemon
    """

    def handle(self):
        if "Fire" in self.pokemon.type:
            self.pokemon.attack = round(self.pokemon.attack * 0.9)
        super().handle()


class BugFlyingTypeModifier(PokemonModifier):
    """
    Increase attack and speed by 10% for bugflying type pokemon
    """

    def handle(self):
        if all(x in self.pokemon.type for x in ["Bug", "Flying"]):
            # print(f"increasing {self.pokemon.name}'s attack and speed by 10%")
            self.pokemon.speed = round(self.pokemon.speed * 1.1)
            self.pokemon.attack = round(self.pokemon.attack * 1.1)
        super().handle()


class InitialGInNameModifier(PokemonModifier):
    """
    If pokemon name starts with "g", Increase defense of pokemon by (name_length - 1) * 5.
    """

    def handle(self):
        if self.pokemon.name.lower().startswith("g"):
            multiplier = len(self.pokemon.name) - 1
            self.pokemon.defense += multiplier * 5
        super().handle()
