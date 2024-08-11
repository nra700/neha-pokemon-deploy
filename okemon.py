import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('pokemon.csv')

# Function to get Pokémon data by name
def get_pokemon_data(name, df):
    pokemon = df[df['name'] == name].to_dict('records')
    if not pokemon:
        raise ValueError(f"Pokémon {name} not found")
    return pokemon[0]

# # Function to calculate damage
# def calculate_damage(attacker, defender, df):
#     type1, type2 = attacker['type1'], attacker['type2']
#     attack = attacker['attack']
    
#     against_type1 = defender[f'against_{type1}']
    
#     if pd.isna(type2):
#         against_type2 = 1  # Default to neutral effect if no type2
#     else:
#         against_type2 = defender[f'against_{type2}']
    
#     damage = (attack / 200) * 100 - (((against_type1 / 4) * 100) + ((against_type2 / 4) * 100))
#     return damage

# Function to simulate a battle
def battle(pokemon_a, pokemon_b):
    # damage_a_to_b = calculate_damage(pokemon_a, pokemon_b, df)
    # damage_b_to_a = calculate_damage(pokemon_b, pokemon_a, df)
    
    # if damage_a_to_b > damage_b_to_a:
    #     return pokemon_a['name'], damage_a_to_b
    # elif damage_b_to_a > damage_a_to_b:
    #     return pokemon_b['name'], damage_b_to_a
    # else:
    #     return "Draw", 0
    if pokemon_a['attack'] > pokemon_b['defense']:
        winner = pokemon_a['name']
        margin = pokemon_a['attack'] - pokemon_b['defense']
    else:
        winner = pokemon_b['name']
        margin = pokemon_b['defense'] - pokemon_a['attack']
    return winner, margin


# Example usage
pokemon_a = get_pokemon_data('Pikachu', df)
pokemon_b = get_pokemon_data('Bulbasaur', df)
winner, margin = battle(pokemon_a, pokemon_b)
print(f"The winner is {winner} with a margin of {margin}")
