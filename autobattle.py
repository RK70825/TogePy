import battle
import pokeStructs
import pkmn_test
import random

def init_game():
    # Fake Battle Values
    battle_vals = dict()
    battle_vals['Level'] = 100
    battle_vals['# Poke'] = 6
    battle_vals['Items'] = True
    battle_vals['Tier'] = 'Uber'
    battle_vals['Players'] = 'CPU vs. CPU'
    
    # Get teams. Random for now.
    team1 = pkmn_test.random_Team()
    team2 = pkmn_test.random_Team()
    
    # Initialize
    team1.init_battle(battle_vals)
    team2.init_battle(battle_vals)
    
    # Location for where battle_vals['# Poke'] will be respected
    
    #
    return

if __name__ == '__main__':
    print 'testing'