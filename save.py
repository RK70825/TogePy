"""
togePy.save

This module saves user created data for togePy
"""

import os
import cPickle as pickle
import pokeStructs

pokePath = os.path.join(os.getcwd(), 'POKE')
teamPath = os.path.join(os.getcwd(), 'TEAM')

# Create PKMN and TEAM folders if they don't exist
if not os.path.isdir(pokePath):
    os.mkdir(pokePath)
if not os.path.isdir(teamPath):
    os.mkdir(teamPath)
    
def get_Files(folder):
    if folder in ('POKE', 'TEAM'):
        path = os.path.join(os.getcwd(), folder)
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        return
    
def save_Poke(poke, saveName='', overwrite=False):
    #Allow to provide a savename and overwriting a pokemon
    if not isinstance(poke, pokeStructs.Pokemon):
        return
    if saveName == '':
        name = poke.Name
        i = 1
        fPath = os.path.join(pokePath, name+'_'+str(i))
        while os.path.isfile(fPath):
            i += 1
            fPath = os.path.join(pokePath, name+'_'+str(i))
    else:
        fPath = os.path.join(pokePath, saveName)
        if os.path.isfile(fPath) and not overwrite:
            return
    with open(fPath, 'wb') as f:
        pickle.dump(poke, f)
        
def load_Poke(fname):
    fPath = os.path.join(pokePath, fname)
    with open(fPath, 'rb') as f:
        poke = pickle.load(f)
    return poke
        
def save_Team(team, saveName='', overwrite=False):
    if not isinstance(team, pokeStructs.Team):
        return
    if saveName == '':
        name = team.Name
        i = 1
        fPath = os.path.join(teamPath, name+'_'+str(i))
        while os.path.isfile(fPath):
            i += 1
            fPath = os.path.join(teamPath, name+'_'+str(i))
    else:
        fPath = os.path.join(teamPath, saveName)
        if os.path.isfile(fPath) and not overwrite:
            return
    with open(fPath, 'wb') as f:
        pickle.dump(team, f)
        
def load_Team(fname):
    fPath = os.path.join(teamPath, fname)
    with open(fPath, 'rb') as f:
        team = pickle.load(f)
    return team