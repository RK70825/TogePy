from pykemon import api
import Pokemon
import pokeStructs
import cPickle as pickle
import requests
import os.path
import time
import sys
from clint.textui import progress

########################################################################
       

class fetcher():
    """Fetch pokedex, move, ability and item data"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
    #----------------------------------------------------------------------
    def update(self, max_file_age=31):
        """Update databases"""
        build_Abilities(max_file_age)
        build_Items(max_file_age)
        build_Moves(max_file_age)
        build_Pokedex(max_file_age)
    
def build_Pokedex(max_file_age = 7):
    age = time.time() - os.path.getmtime('pokedex')
    age = age/(86400)
    if age <= max_file_age:
        print 'Pokedex up to date'
        sys.stdout.write('Pokedex up to date')
        sys.stdout.flush()
        return
    
    Pokedex = {}
    
    print 'Building Pokedex'
    for i in progress.bar(range(1,719)):
        poke = api.get(pokemon_id=str(i))
        Name = str(poke.name)
        ID = int(poke.id)
        Types = map(str, poke.types.keys())
        Tier = 'None'
        Abilities = map(str, poke.abilities.keys())
        BaseStats = Pokemon.createBS(map(int, [poke.hp, poke.attack, poke.defense, poke.sp_atk, 
                                               poke.sp_def, poke.speed]))
        Height = str(poke.height)
        Weight = str(poke.weight)
        Pokedex[ID] = pokeStructs.Pokemon_dex(Name, ID, Types, Tier, Abilities, BaseStats, Height, Weight)
        
    with open('pokedex', 'wb') as f:
        pickle.dump(Pokedex, f)
    print 'Pokedex Saved!'
    return

def build_Moves(max_file_age = 7):
    age = time.time() - os.path.getmtime('moves')
    age = age/(86400)
    if age <= max_file_age:
        print 'Moves up to date'
        return
    
    Moves = {}
    
    print 'Building Moves'
    url = 'http://www.smogon.com/bw/moves/'
    r = requests.get(url)
    move_data = r.content
    
    move_data = move_data.split('move_list')[1]
    move_data = move_data.split('<a href')[1:]
    
    for i in progress.bar(range(len(move_data))):
        m = move_data[i]
        m = m.split('<td>')
        link, Name = m[0].split('/bw/moves/')[1].split('</a>')[0].split('">')
        link = 'http://www.smogon.com/bw/moves/' + link
        Power = m[1].split('<')[0]
        Accuracy = m[2].split('</td>')[0].split('%')[0]
        PP = m[3].split('<')[0]
        Target = m[4].strip().split('\n')[0]
        Description = m[5].split('</td')[0]
        m2 = requests.get(link)
        m2 = m2.content
        s = '<h1>' + Name + '</h1>'
        m2 = m2.split(s)[1].split('</table>')[0]
        m2 = m2.split('<td>')[1:]
        Type = m2[0].split('">')[1].split('</a>')[0]
        Priority = m2[4].split('</td>')[0]
        Damage = m2[5].strip().split('\n')[0]
        Moves[Name] = pokeStructs.Move(Name, Type, Power, Accuracy, Priority, PP, 
                                  Target, Description, Damage)
        
    with open('moves', 'wb') as f:
        pickle.dump(Moves, f)
    print 'Moves Saved!'
    return
    
def build_Abilities(max_file_age = 7):
    age = time.time() - os.path.getmtime('abilities')
    age = age/(86400)
    if age <= max_file_age:
        print 'Abilities up to date'
        return
    
    Abilities = {}
    
    print 'Building Abilities'
    url = 'http://www.smogon.com/bw/abilities/'
    r = requests.get(url)
    r = r.content
    
    abils = r.split('ability_list')[1]
    abils = abils.split('<a href')[1:]
    
    for i in progress.bar(range(len(abils))):
        a = abils[i]
        a = a.split('<td>')
        Name = a[0].split('/bw/abilities/')[1].split('</a>')[0].split('">')[1].lower()
        Description = a[1].split('</td>')[0]
        Abilities[Name] = Description
    
    with open('abilities', 'wb') as f:
        pickle.dump(Abilities, f)
    print 'Abilities Saved'
    return
    
def build_Items(max_file_age = 7):
    age = time.time() - os.path.getmtime('items')
    age = age/(86400)
    if age <= max_file_age:
        print 'Items up to date'
        return
    
    Items = {}
    
    print 'Building Items'
    url = 'http://www.smogon.com/bw/items/'
    r = requests.get(url)
    r = r.content
    
    its = r.split('item_list')[1]
    its = its.split('<a href')[1:]
    
    for i in progress.bar(range(len(its))):
        i = its[i]
        i = i.split('<td>')
        link, Name = i[0].split('="')[1].split('</a>')[0].split('">')
        link = 'http://www.smogon.com' + link
        info = requests.get(link).content
        s = '<h1>' + Name + '</h1>'
        info = info.split(s)[1].strip()
        Description = info.split('<p>')[1].split('</p>')[0]
        Items[Name] = Description
        
    with open('items', 'wb') as f:
        pickle.dump(Items, f)
    print 'Items Saved'
    return

if __name__=='__main__':
    if len(sys.argv) == 1:
        sys.exit('Inputs required')
    elif len(sys.argv) == 2:
        try:
            age = int(sys.argv[1])
            f = fetcher()
            f.update(age)
        except ValueError:
            sys.exit('Positive Integer Input Required')
    else:
        sys.exit('Too many arguments')