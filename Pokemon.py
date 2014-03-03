import numpy as np
import heapq

class Pokemon_dex:
    def __init__(self, Name, ID, Type, Tier, Abilities, BaseStats, Height, 
                 Weight):
        self.Name = str(Name)
        self.ID = int(ID)
        self.Type = Type
        self.Tier = str(Tier)
        self.Abilities = Abilities
        self.BaseStats = dict(BaseStats)
        self.Height = float(Height)
        self.Weight = float(Weight)

class Pokemon(Pokemon_dex):
    def __init__(self, p_dex, Level, BaseStats, EVs, IVs, Nature, Happiness, 
                 Ability, Moves):
        Pokemon_dex.__init__(self, p_dex.Name, p_dex.ID, p_dex.Type, p_dex.Tier,
                            p_dex.Abilities, p_dex.BaseStats, p_dex.Height, 
                            p_dex.Weight)
        self.p_dex = p_dex
        self.Level = int(Level)
        self.EVs = dict(EVs)
        self.IVs = dict(IVs)
        self.NatureName = str(Nature)
        self.Nature = dict(calcNature(Nature))
        self.Happiness = int(Happiness)
        self.Stats = dict(self.calcStats())
        self.DefType = dict(calcDefType(self.Type))
        self.Moves = Moves
        
    def calcStats(self):
        d_Stats = {}
        d_Stats['HP'] = np.floor((self.IVs['HP'] + (2*self.BaseStats['HP']) + 
                                  self.EVs['HP']/4 + 100)*self.Level/100) + 10
        for stat in ('Atk', 'Def', 'SpA', 'SpD', 'Spe'):
            d_Stats[stat] = np.floor(self.Nature[stat]*(((self.IVs[stat] + 
                                    (2*self.BaseStats[stat]) + 
                                    self.EVs[stat]/4)*self.Level/100)+5))
        return d_Stats
    
class Pokemon_battle(Pokemon):
    def __init__(self, pkmn):
        Pokemon.__init__(self, pkmn.p_dex, pkmn.Level, pkmn.BaseStats, pkmn.EVs, 
                        pkmn.IVs, pkmn.Nature, pkmn.Happiness, pkmn.Ability,
                        pkmn.Moves)
        self.b_Stats = self.Stats
        self.Status = None
        self.Fainted = False
        
########################################################################
class Team:
    """Pokemon Team"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.Members = dict()
        self.Nmems = 0
        
    #----------------------------------------------------------------------
    def set_Member(self, poke, pos):
        """Set a member of the team, update Nmems"""
        if not isinstance(poke, Pokemon_battle):
            return
        if not isinstance(pos, int) and pos in range(1,7):
            return
        self.Members[pos] = poke
        self.Nmems = len(self.Members.keys())
        
    #----------------------------------------------------------------------
    def get_Member(self, pos):
        """Return member at position 'pos'."""
        if not isinstance(pos, int) and pos in range(1,7):
            return "Argument pos should be type 'int' and valued 1:6"
        if not pos in self.Members.keys():
            return "Position filled"
        return self.Members[pos]
        
    #----------------------------------------------------------------------
    def pos_open(self, pos):
        """Checks if a position is open on a team"""
        if not isinstance(pos, int) and pos in range(1,7):
            return "Argument pos should be type 'int' and valued 1:6"
        if pos in self.Members.keys():
            return False
        else:
            return True
        
class Move:
    def __init__(self, Name, Type, Power, Accuracy, Priority, PP, Target, 
                 Description, Damage):
        self.Name = str(Name)
        self.Type = str(Type).lower().capitalize()
        if Power == '-':
            self.Power = None
        else:
            self.Power = float(Power)
        if Accuracy == '-':
            self.Accuracy = None
        else:
            self.Accuracy = float(Accuracy)
        self.Priority = int(Priority)
        self.PP = int(PP)
        self.Target = str(Target)
        self.Description = str(Description)
        self.Damage = str(Damage).lower()
        
########################################################################
class Moveset:
    """Valid Moveset"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self. Moves = dict()
        self.Nmovs = 0
        
    #----------------------------------------------------------------------
    def set_Move(self, move, pos):
        """Set a move, update Nmovs"""
        if not isinstance(poke, Move):
            return
        if not isinstance(pos, int) and pos in range(1,5):
            return
        self.Moves[pos] = poke
        self.Nmovs = len(self.Moves.keys())
        
    #----------------------------------------------------------------------
    def get_Move(self, pos):
        """Return move at position 'pos'."""
        if not isinstance(pos, int) and pos in range(1,5):
            return "Argument pos should be type 'int' and valued 1:4"
        if not pos in self.Moves.keys():
            return "Position filled"
        return self.Moves[pos]
        
    #----------------------------------------------------------------------
    def pos_open(self, pos):
        """Checks if a position is open in the moveset"""
        if not isinstance(pos, int) and pos in range(1,5):
            return "Argument pos should be type 'int' and valued 1:4"
        if pos in self.Moves.keys():
            return False
        else:
            return True
        
def createBS(l_BStats):
    d_BaseStats = {}
    d_BaseStats['HP'] = float(l_BStats[0])
    d_BaseStats['Atk'] = float(l_BStats[1])
    d_BaseStats['Def'] = float(l_BStats[2])
    d_BaseStats['SpA'] = float(l_BStats[3])
    d_BaseStats['SpD'] = float(l_BStats[4])
    d_BaseStats['Spe'] = float(l_BStats[5])
    return d_BaseStats

def createEVs(l_EVs = (0,0,0,0,0,0)):
    d_EVs = {}
    d_EVs['HP'] = float(l_EVs[0])
    d_EVs['Atk'] = float(l_EVs[1])
    d_EVs['Def'] = float(l_EVs[2])
    d_EVs['SpA'] = float(l_EVs[3])
    d_EVs['SpD'] = float(l_EVs[4])
    d_EVs['Spe'] = float(l_EVs[5])
    return d_EVs

def createIVs(l_IVs = (15,15,15,15,15,15)):
    d_IVs = {}
    d_IVs['HP'] = float(l_IVs[0])
    d_IVs['Atk'] = float(l_IVs[1])
    d_IVs['Def'] = float(l_IVs[2])
    d_IVs['SpA'] = float(l_IVs[3])
    d_IVs['SpD'] = float(l_IVs[4])
    d_IVs['Spe'] = float(l_IVs[5])
    return d_IVs

def calcNature(Nature):
    d_Nature = {'HP': 1.0, 'Atk': 1.0, 'SpD': 1.0, 'Def': 1.0, 'Spe': 1.0, 
                'SpA': 1.0}
    if Nature == 'Lonely':
        d_Nature['Atk'] = 1.1
        d_Nature['Def'] = 0.9
    elif Nature == 'Brave':
        d_Nature['Atk'] = 1.1
        d_Nature['Spe'] = 0.9
    elif Nature == 'Adamant':
        d_Nature['Atk'] = 1.1
        d_Nature['SpA'] = 0.9
    elif Nature == 'Naughty':
        d_Nature['Atk'] = 1.1
        d_Nature['SpD'] = 0.9
    elif Nature == 'Bold':
        d_Nature['Def'] = 1.1
        d_Nature['Atk'] = 0.9
    elif Nature == 'Relaxed':
        d_Nature['Def'] = 1.1
        d_Nature['Spe'] = 0.9
    elif Nature == 'Impish':
        d_Nature['Def'] = 1.1
        d_Nature['SpA'] = 0.9
    elif Nature == 'Lax':
        d_Nature['Def'] = 1.1
        d_Nature['SpD'] = 0.9
    elif Nature == 'Timid':
        d_Nature['Spe'] = 1.1
        d_Nature['Atk'] = 0.9
    elif Nature == 'Hasty':
        d_Nature['Spe'] = 1.1
        d_Nature['Def'] = 0.9
    elif Nature == 'Jolly':
        d_Nature['Spe'] = 1.1
        d_Nature['SpA'] = 0.9
    elif Nature == 'Naive':
        d_Nature['Spe'] = 1.1
        d_Nature['SpD'] = 0.9
    elif Nature == 'Modest':
        d_Nature['SpA'] = 1.1
        d_Nature['Atk'] = 0.9
    elif Nature == 'Mild':
        d_Nature['SpA'] = 1.1
        d_Nature['Def'] = 0.9
    elif Nature == 'Quiet':
        d_Nature['SpA'] = 1.1
        d_Nature['Spe'] = 0.9
    elif Nature == 'Rash':
        d_Nature['SpA'] = 1.1
        d_Nature['SpD'] = 0.9
    elif Nature == 'Calm':
        d_Nature['SpD'] = 1.1
        d_Nature['Atk'] = 0.9
    elif Nature == 'Gentle':
        d_Nature['SpD'] = 1.1
        d_Nature['Def'] = 0.9
    elif Nature == 'Sassy':
        d_Nature['SpD'] = 1.1
        d_Nature['Spe'] = 0.9
    elif Nature == 'Careful':
        d_Nature['SpD'] = 1.1
        d_Nature['SpA'] = 0.9
    return d_Nature

def calcIV(stat, EV, nat, lv, BS, HP = False):
    if not HP:
        return ((stat/nat) - 5)*(100/lv) - 2*BS - EV/4
    else:
        return "Not Supported Yet"

def printTypeEff(pType):
    d_TypeEff = calcDefType(pType)
    Immune = []
    Resistant = []
    Normal = []
    Weak = []
    for t in d_TypeEff.keys():
        if d_TypeEff[t] == 0:
            Immune.append((t, d_TypeEff[t]))
        elif d_TypeEff[t] in (0.25, 0.5):
            Resistant.append((t, d_TypeEff[t]))
        elif d_TypeEff[t] == 1:
            Normal.append((t, d_TypeEff[t]))
        elif d_TypeEff[t] in (2, 4):
            Weak.append((t, d_TypeEff[t]))
        else:
            print "Lul wut? %s" %(t)
            
    if Normal:
        print "Normal"
        for n in Normal:
            print "    %s - %f" %(n[0], n[1])
    if Weak:
        print "Weak"
        for w in Weak:
            print "    %s - %f" %(w[0], w[1])
    if Immune:
        print "Immune"
        for i in Immune:
            print "    %s - %f" %(i[0], i[1])
    if Resistant:
        print "Resistant"
        for r in Resistant:
            print "    %s - %f" %(r[0], r[1])

def calcTypeEff(Types):
    d_TypeEff = {'Normal': 1, 'Fighting': 1, 'Flying': 1, 'Poison': 1, 
                 'Ground': 1, 'Rock': 1, 'Bug': 1, 'Ghost': 1, 'Steel': 1, 
                 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 1,
                 'Ice': 1, 'Dragon': 1, 'Dark': 1, 'Fairy': 1}
    if 'Normal' in Types:
        d_TypeEff['Rock'] *= 0.5
        d_TypeEff['Ghost'] *= 0
        d_TypeEff['Steel'] *= 0.5
    if 'Fighting' in Types:
        d_TypeEff['Normal'] *= 2
        d_TypeEff['Flying'] *= 0.5
        d_TypeEff['Poison'] *= 0.5
        d_TypeEff['Rock'] *= 2
        d_TypeEff['Bug'] *= 0.5
        d_TypeEff['Ghost'] *= 0
        d_TypeEff['Steel'] *= 2
        d_TypeEff['Psychic'] *= 0.5
        d_TypeEff['Ice'] *= 2
        d_TypeEff['Dark'] *= 2
        d_TypeEff['Fairy'] *= 0.5
    if 'Flying' in Types:
        d_TypeEff['Fighting'] *= 2
        d_TypeEff['Rock'] *= 0.5
        d_TypeEff['Bug'] *= 2
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Grass'] *= 2
        d_TypeEff['Electric'] *= 0.5
    if 'Poison' in Types:
        d_TypeEff['Poison'] *= 0.5
        d_TypeEff['Ground'] *= 0.5
        d_TypeEff['Rock'] *= 0.5
        d_TypeEff['Ghost'] *= 0.5
        d_TypeEff['Steel'] *= 0
        d_TypeEff['Grass'] *= 2
        d_TypeEff['Fairy'] *= 2
    if 'Ground' in Types:
        d_TypeEff['Flying'] *= 0
        d_TypeEff['Poison'] *= 2
        d_TypeEff['Rock'] *= 2
        d_TypeEff['Bug'] *= 0.5
        d_TypeEff['Steel'] *= 2
        d_TypeEff['Fire'] *= 2
        d_TypeEff['Grass'] *= 0.5
        d_TypeEff['Electric'] *= 2
    if 'Rock' in Types:
        d_TypeEff['Fighting'] *= 0.5
        d_TypeEff['Flying'] *= 2
        d_TypeEff['Ground'] *= 0.5
        d_TypeEff['Bug'] *= 2
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Fire'] *= 2
        d_TypeEff['Ice'] *= 2
    if 'Bug' in Types:
        d_TypeEff['Fighting'] *= 0.5
        d_TypeEff['Flying'] *= 0.5
        d_TypeEff['Poison'] *= 0.5
        d_TypeEff['Ghost'] *= 0.5
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Fire'] *= 0.5
        d_TypeEff['Grass'] *= 2
        d_TypeEff['Psychic'] *= 2
        d_TypeEff['Dark'] *= 2
        d_TypeEff['Fairy'] *= 0.5
    if 'Ghost' in Types:
        d_TypeEff['Normal'] *= 0
        d_TypeEff['Ghost'] *= 2
        d_TypeEff['Psychic'] *= 2
        d_TypeEff['Dark'] *= 0.5
    if 'Steel' in Types:
        d_TypeEff['Rock'] *= 2
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Fire'] *= 0.5
        d_TypeEff['Water'] *= 0.5
        d_TypeEff['Electric'] *= 0.5
        d_TypeEff['Ice'] *= 2
        d_TypeEff['Fairy'] *= 2
    if 'Fire' in Types:
        d_TypeEff['Rock'] *= 0.5
        d_TypeEff['Bug'] *= 2
        d_TypeEff['Steel'] *= 2
        d_TypeEff['Fire'] *= 0.5
        d_TypeEff['Water'] *= 0.5
        d_TypeEff['Grass'] *= 2
        d_TypeEff['Ice'] *= 2
        d_TypeEff['Dragon'] *= 0.5
    if 'Water' in Types:
        d_TypeEff['Ground'] *= 2
        d_TypeEff['Rock'] *= 2
        d_TypeEff['Fire'] *= 2
        d_TypeEff['Water'] *= 0.5
        d_TypeEff['Grass'] *= 0.5
        d_TypeEff['Dragon'] *= 0.5
    if 'Grass' in Types:
        d_TypeEff['Flying'] *= 0.5
        d_TypeEff['Poison'] *= 0.5
        d_TypeEff['Ground'] *= 2
        d_TypeEff['Rock'] *= 2
        d_TypeEff['Bug'] *= 0.5
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Fire'] *= 0.5
        d_TypeEff['Water'] *= 2
        d_TypeEff['Grass'] *= 0.5
        d_TypeEff['Dragon'] *= 0.5
    if 'Electric' in Types:
        d_TypeEff['Flying'] *= 2
        d_TypeEff['Ground'] *= 0
        d_TypeEff['Water'] *= 2
        d_TypeEff['Grass'] *= 0.5
        d_TypeEff['Electric'] *= 0.5
        d_TypeEff['Dragon'] *= 0.5
    if 'Psychic' in Types:
        d_TypeEff['Fighting'] *= 2
        d_TypeEff['Poison'] *= 2
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Psychic'] *= 0.5
        d_TypeEff['Dark'] *= 0
    if 'Ice' in Types:
        d_TypeEff['Flying'] *= 2
        d_TypeEff['Ground'] *= 2
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Fire'] *= 0.5
        d_TypeEff['Water'] *= 0.5
        d_TypeEff['Grass'] *= 2
        d_TypeEff['Ice'] *= 0.5
        d_TypeEff['Dragon'] *= 2
    if 'Dragon' in Types:
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Dragon'] *= 2
        d_TypeEff['Fairy'] *= 0
    if 'Dark' in Types:
        d_TypeEff['Fighting'] *= 0.5
        d_TypeEff['Ghost'] *= 2
        d_TypeEff['Psychic'] *= 2
        d_TypeEff['Dark'] *= 0.5
        d_TypeEff['Fairy'] *= 0.5
    if 'Fairy' in Types:
        d_TypeEff['Fighting'] *= 2
        d_TypeEff['Poison'] *= 0.5
        d_TypeEff['Steel'] *= 0.5
        d_TypeEff['Fire'] *= 0.5
        d_TypeEff['Dragon'] *= 2
        d_TypeEff['Dark'] *= 2
    return d_TypeEff

def calcDefType(Types):
    d_defTypes = {'Normal': 1, 'Fighting': 1, 'Flying': 1, 'Poison': 1, 
                  'Ground': 1, 'Rock': 1, 'Bug': 1, 'Ghost': 1, 'Steel': 1, 
                  'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 
                  'Psychic': 1, 'Ice': 1, 'Dragon': 1, 'Dark': 1, 'Fairy': 1}
    for defType in Types:
        for offType in ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 
                        'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 
                        'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark',
                        'Fairy']:
            d_defTypes[offType] *= calcTypeEff([offType])[defType]
    return d_defTypes

def calcSTABTypings(Types):
    d_STABTypes = {}
    for t in Types:
        if d_STABTypes:
            d_newType = calcTypeEff([t])
            for typ in d_STABTypes.keys():
                if d_newType[typ] > d_STABTypes[typ]:
                    d_STABTypes[typ] = d_newType[typ]
        else:
            d_STABTypes = calcTypeEff([t])
    return d_STABTypes
        
def calcDamage(user, target, move):
    # Calc Target Info
    uLvl = user.Level
    if move.mType == 'Physical':
        uAtk = user.Stats['Atk']
        tDef = target.Stats['Def']
    elif move.mType == 'Special':
        uAtk = user.Stats['SpA']
        tDef = target.Stats['SpD']
    base = move.Power
    # Calc Modifier
    if move.Type in user.Type:
        STAB = 1.5
    else:
        STAB = 1.0
    typeEff = target.DefType[move.Type]
    rnd = 0.85 + 0.15*np.random.rand()
    if np.random.rand() < 0.0625:
        crit = 1.5
    else:
        crit = 1
    modifier = STAB*typeEff*rnd*crit
    # Calc Damage
    dmg = (((2*uLvl + 10)/250)*(uAtk/tDef)*base + 2)*modifier
    return np.floor(dmg)

def dmgStats(user, target, move, iters):
    dmgs = []
    for i in range(iters):
        dmgs.append(calcDamage(user, target, move))
    dmean = np.mean(dmgs)
    dstd = np.std(dmgs)
    dmedian = np.median(dmgs)
    dmin = min(dmgs)
    dmax = max(dmgs)
    drange = dmax - dmin
    return dmean, dstd, dmedian, dmin, dmax, drange

def f1(a, b):
    return (2*a*b)/(a + b)

def off_f1(a, b):
    return np.mean([f1(a, b), max([a, b])])