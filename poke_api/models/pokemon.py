from collections import OrderedDict
from enum import Enum
from . import db


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


class Pokemon(db.Model):

    __tablename__ = 'Pokemon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    hp = db.Column(db.Integer, nullable=False)
    type_1 = db.Column(db.Enum(PokemonType), nullable=False)
    type_2 = db.Column(db.Enum(PokemonType))
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    special_attack = db.Column(db.Integer, nullable=False)
    special_defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    generation = db.Column(db.Integer)
    legendary = db.Column(db.Boolean)

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

    @property
    def to_python(self):
        public_attributes = ["id", "name", "attack",
                             "defense", "hp", "primary_type",
                             "secondary_type", "speed",
                             "special_attack", "special_defense",
                             "generation", "legendary"]

        return OrderedDict([k, getattr(self, k)] for k in public_attributes)