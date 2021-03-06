'''
togePy.battle

This module handles the battle sequence in togePy
'''

import numpy
from math import floor as fl
import random

def turn_priority(action):
    if action[0] == 'switch':
        return -1
    else:
        return 0

def compare_speed(pk1, pk2):
    if pk1.Stats['Spe'] > pk2.Stats['Spe']:
        return 1
    elif pk2.Stats['Spe'] > pk1.Stats['Spe']:
        return 2
    else:
        return int(round(random.random()))

def calc_Damage(attacker, defender, move):
    #todo: Include a check to determine if the move has a special damage formula, such as Seismic Toss or Dragon Rage
    L = attacker.Level
    #todo: Add support for variable base power
    P = move.Power
    #todo: Include checks on multipliers for stats
    if move.Damage == 'physical':
        A = attacker.Stats['Atk']
        D = defender.Stats['Def']
    else:
        A = attacker.Stats['SpA']
        D = defender.Stats['SpD']
    dmg = fl(fl(fl(2 * L / 5 + 2) * A * P / D) / 50) + 2
    t = [i.lower().capitalize() for i in attacker.Type]
    if move.Type in t:
        dmg *= 1.5
    dmg *= defender.DefType[move.Type]
    
    R = random.choice(range(16))
    rand_mult = float(100-R)/100
    dmg *= rand_mult
    
    return int(dmg)

def acc_check(move):
    '''
    Returns True if the move hits, False otherwise
    '''
    acc = move.Accuracy
    if acc == None:
        acc = 1.0
    else:
        acc /= 100.0
    return acc > random.random()