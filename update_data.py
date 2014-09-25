from pykemon import api
import Pokemon
import pokeStructs
import cPickle as pickle
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import unicodedata
import os.path, time
import sys
import re
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
        
def smogonTable(url):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(0.5)
    more2load = True
    while more2load:
        old_len = len(driver.page_source)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        new_len = len(driver.page_source)
        if old_len == new_len:
            more2load = False
    table = driver.find_element_by_xpath('//table/tbody')
    driver.close()
    table_html = table.get_attribute('innerHTML')
    soup = BeautifulSoup(table_html)
    table2 = soup.find_all('td')
    return table2

def checkAge(fname, max_age):
    age = time.time() - os.path.getmtime(fname)
    age = age/86400
    if age <= max_age:
        print '%s up to date' %(fname)
    else:
        print 'Building %s' %(fname)
    return age <= max_age

def toAscii(unicodestr):
    return unicodedata.normalize('NFKD', unicodestr).encode('ascii', 'ignore')

def build_Abilities(max_file_age = 7):
    if checkAge('abilities', max_file_age):
        return
    
    abilTable = smogonTable('http://www.smogon.com/dex/xy/abilities/')
    keys = [toAscii(x.get_text()) for x in abilTable[::2]]
    vals = [toAscii(x.get_text()) for x in abilTable[1::2]]
    Abilities = dict(zip(keys, vals))
    
    with open('abilities', 'wb') as f:
        pickle.dump(Abilities, f)
    print 'Abilities Saved'
    return

def build_Items(max_file_age = 7):
    if checkAge('items', max_file_age):
        return
    
    itemTable = smogonTable('http://www.smogon.com/dex/xy/items/')
    keys = [toAscii(x.get_text()) for x in itemTable[::2]]
    vals = [toAscii(x.get_text()) for x in itemTable[1::2]]
    Items = dict(zip(keys, vals))
        
    with open('items', 'wb') as f:
        pickle.dump(Items, f)
    print 'Items Saved'
    return

def build_Moves(max_file_age = 7):
    if checkAge('moves', max_file_age):
        return
    
    Moves = {}
    moveTable = smogonTable('http://www.smogon.com/dex/xy/moves/')
    
    for i in progress.bar(range(len(moveTable)/7)):
        Name = toAscii(moveTable[7*i].get_text())
        Type = toAscii(moveTable[7*i+1].get_text())
        Damage = toAscii(moveTable[7*i+2].findAll("div")[0]['class'][1])
        Power = toAscii(moveTable[7*i+3].get_text())[5:]
        if Power == '':
            Power = '-'
        Accuracy = toAscii(moveTable[7*i+4].get_text())[8:-1]
        if Accuracy == '':
            Accuracy = '-'
        PP = toAscii(moveTable[7*i+5].get_text())[2:]
        Description = toAscii(moveTable[7*i+6].get_text())
        Priority = 0
        Target = 'self'
        Moves[Name] = pokeStructs.Move(Name, Type, Power, Accuracy, Priority, 
                                      PP, Target, Description, Damage)
        
    with open('moves', 'wb') as f:
            pickle.dump(Moves, f)
            print 'Moves Saved!'
    return    

def build_Pokedex(max_file_age = 7):
    if checkAge('pokedex', max_file_age):
        return
    
    Pokedex = {}
    pokeTable = smogonTable('http://www.smogon.com/dex/xy/pokemon/')
    
    for i in progress.bar(range(len(pokeTable)/11)):
        Name = toAscii(pokeTable[11*i].get_text())
        Types = toAscii(pokeTable[11*i+1].get_text())
        Types = re.findall('[A-Z][^A-Z]*', Types)
        Abilities = pokeTable[11*i+2].findAll('span')[::2]
        Abilities += pokeTable[11*i+3].findAll('span')[::2]
        Abilities = [toAscii(a.get_text()) for a in Abilities]
        Tier = toAscii(pokeTable[11*i+4].get_text())
        HP = toAscii(pokeTable[11*i+5].get_text())[2:]
        Atk = toAscii(pokeTable[11*i+6].get_text())[3:]
        Def = toAscii(pokeTable[11*i+7].get_text())[3:]
        SpA = toAscii(pokeTable[11*i+8].get_text())[3:]
        SpD = toAscii(pokeTable[11*i+9].get_text())[3:]                        
        Spe = toAscii(pokeTable[11*i+10].get_text())[3:]
        BaseStats = Pokemon.createBS(map(int, [HP, Atk, Def, SpA, SpD, Spe]))
                    
    for i in progress.bar(range(1,719)):
        poke = api.get(pokemon_id=str(i))
        Name = str(poke.name)
        ID = int(poke.id)
        Types = map(str, poke.types.keys())
        Tier = 'None'
        Abilities = map(str, poke.abilities.keys())
        BaseStats = Pokemon.createBS(map(int, [poke.hp, poke.attack, 
                                               poke.defense, poke.sp_atk, 
                                               poke.sp_def, poke.speed]))
        Height = str(poke.height)
        Weight = str(poke.weight)
        Pokedex[ID] = pokeStructs.Pokemon_dex(Name, ID, Types, Tier, Abilities, 
                                              BaseStats, Height, Weight)
        
    with open('pokedex', 'wb') as f:
        pickle.dump(Pokedex, f)
    print 'Pokedex Saved!'
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