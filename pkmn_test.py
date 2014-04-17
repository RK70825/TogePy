"""
togePy.pkmn_test

This module tests functionality for togePy
"""

import pokeStructs
import cPickle as pickle
import random
import numpy as np

# Load Data
with open('pokedex', 'rb') as f:
    pokedex = pickle.load(f)
with open('abilities', 'rb') as f:
    abilities = pickle.load(f)
with open('items', 'rb') as f:
    items = pickle.load(f)
with open('moves', 'rb') as f:
    moves = pickle.load(f)
    
# Create Test Data Suite
def random_Move(only_dmg = True):
    if only_dmg:
        is_dmg = False
        while is_dmg == False:
            m = moves[random.choice(moves.keys())]
            is_dmg = (m.Damage in ('physical', 'special'))
        return m
    else:
        return moves[random.choice(moves.keys())]
                 
def random_Moveset(only_dmg = True):
    ms = pokeStructs.Moveset()
    ms.set_All([random_Move(only_dmg) for _ in xrange(4)])
    return ms

def random_Poke():
    def random_EVs():
        EV = np.random.randint(256, size=6).astype(float)
        while EV.sum() != 510 or any(EV > 255):
            EV_old = EV
            if EV.sum() != 510:
                EV = np.round(510./EV.sum()*EV)
            EV[EV > 255] = 255
            if all(EV_old == EV):
                EV = np.random.randint(256, size=6).astype(float)
        return pokeStructs.createEVs(EV.astype(int).tolist())
    def random_IVs():
        return pokeStructs.createIVs(np.random.randint(32, size=6).tolist())
    def random_Nature():
        return random.choice(['Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty', 'Bold', 'Docile', 'Relaxed', 'Impish', 'Lax', 'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive', 'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash', 'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky'])
    def random_Happiness():
        return random.randint(0,255)
    def random_Ability():
        return random.choice(p_dex.Abilities)
    def random_Moves():
        return random_Moveset()
    p_dex = pokedex[random.choice(pokedex.keys())]
    p = pokeStructs.Pokemon(p_dex, np.random.randint(1, 101), random_EVs(), random_IVs(), random_Nature(), random_Happiness(), random_Ability(), random_Moves(), random.choice(items.keys()))
    p.CurHP = int(np.round(p.CurHP * np.random.random()))
    p.Status = random.choice([None, 'FZN', 'PAR', 'SLP', 'PSN', 'BRN'])
    return p

def random_Team():
    t = pokeStructs.Team('Random Team')
    t.set_All([random_Poke() for _ in xrange(6)])
    return t

def restore_Team(t):
    for p in t.Members.values():
        p.CurHP = p.Stats['HP']
        p.Status = None
        
def nature_list():
    l_natures = ['Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty', 'Bold', 'Docile', 'Relaxed', 'Impish', 'Lax', 'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive', 'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash', 'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky']
    return l_natures
    
if __name__ == '__main__':
    print 'Ready'