'''
togePy.battle

This module handles the battle sequence in togePy
'''

import numpy
from math import floor as fl

def turn_priority(action):
    return 0

def compare_speed(pk1, pk2):
    if pk1.Stats['Spe'] > pk2.Stats['Spe']:
        return 1
    else:
        return 2

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
    dmg = int(dmg)
    return dmg