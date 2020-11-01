from enum import Enum


class PokemonType(Enum):
    Bug = 1
    Dark = 2
    Dragon = 3
    Electric = 4
    Fairy = 5
    Fighting = 6
    Fire = 7
    Flying = 8
    Grass = 9
    Ground = 10
    Ice = 11
    Normal = 12
    Poison = 13
    Psychic = 14
    Rock = 15
    Steel = 16
    Water = 17


class BasePokemon:

    def __init__(self, name='', type_1='', type_2='', total=0, hp=0, attack=0,
                 defense=0, special_attack=0, special_defense=0, speed=0,
                 generation=0, legendary=False, *args, **kwargs):
        self.name = name
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.generation = generation
        self.legendary = legendary

        pokemon_types = iter([PokemonType[t].value for t in [type_1.capitalize(), type_2.capitalize()]
                              if t in PokemonType._member_names_])

        # default to normal type of invalid types were provided
        self.type_1 = next(pokemon_types, PokemonType.Normal.value)
        self.type_2 = next(pokemon_types, None)

    def __str__(self):
        return self.name

    @property
    def primary_type(self):
        return PokemonType(self.type_1).name

    @property
    def secondary_type(self):
        # secondary type is optional
        return PokemonType(self.type_2).name if self.type_2 else None

    @property
    def type(self):
        if self.secondary_type:
            return (self.primary_type, self.secondary_type)
        return self.primary_type,


class Pokemon(BasePokemon):

    def __init__(self, pokemon_data: dict, *args, **kwargs):
        super(Pokemon, self).__init__(**pokemon_data)
