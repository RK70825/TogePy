"""
togePy.formulas

This module stores the formulas required for togePy
"""

from math import floor as fl

def calc_Damage(attacker, defender, move):
    #todo: Include a check to determine if the move has a special damage formula, such as Seismic Toss or Dragon Rage
    L = attackers.Level
    #todo: Add support for variable base power
    P = move.Power
    #todo: Include checks on multipliers for stats
    if move.Damage == 'physical':
        A = attacker.Stats['Atk']
        D = defender.Stats['Def']
    else:
        A = attacker.Stats['SpA']
        D = defender.Stats['SpD']
    return fl(fl(fl(2 * L / 5 + 2) * A * P / D) / 50) + 2