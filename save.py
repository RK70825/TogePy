"""
togePy.save

This module saves user created data for togePy
"""

import os
import cPickle as pickle
from datetime import datetime

pokePath = os.path.join(os.getcwd(), 'POKE')
teamPath = os.path.join(os.getcwd(), 'TEAM')
gamePath = os.path.join(os.getcwd(), 'GAMES')

# Create folders if they don't exist
if not os.path.isdir(pokePath):
    os.mkdir(pokePath)
if not os.path.isdir(teamPath):
    os.mkdir(teamPath)
if not os.path.isdir(gamePath):
    os.mkdir(gamePath)
    
def get_Files(folder):
    if folder in ('POKE', 'TEAM'):
        path = os.path.join(os.getcwd(), folder)
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        return
    
def save_Poke(poke, saveName='', overwrite=False):
    #Allow to provide a savename and overwriting a pokemon
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
    with open(fPath, 'rU') as f:
        s = f.read().replace('\r\n', '\n')
        poke = pickle.loads(s)
    return poke
        
def save_Team(team, saveName='', overwrite=False):
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
    with open(fPath, 'rU') as f:
        s = f.read().replace('\r\n', '\n')
        team = pickle.loads(s)
    return team

def create_game_dir():
    dir_name = 'Game ' + str(datetime.now()).replace(':','.').replace('.','_')
    game_dir = os.path.join(gamePath, dir_name)
    if not os.path.isdir(game_dir):
        os.mkdir(game_dir)
        # Should decide what to do for overwrite directories
    return game_dir

def save_Game(game):
    save_dir = game.save_dir
    fname = str(datetime.now()).replace(':','.').replace('.','_')
    fPath = os.path.join(save_dir, fname)
    with open(fPath, 'wb') as f:
        pickle.dump(game, f)
    return 