"""
togePy.extract_feats

This module extracts features of various togePy data structures.
"""
import pokeStructs
from copy import deepcopy

class pokeExtractor:
    """Extracts features from a Pokemon"""
    
    #----------------------------------------------------------------------
    def __init__(self, poke, isBattle=False, prefix=''):
        """pokeExtractor Constructor"""
        assert isinstance(poke, pokeStructs.Pokemon), 'Must be a Pokemon'
        assert isinstance(isBattle, bool), 'Battle Flag must be boolean'
        assert isinstance(prefix, str), 'Key prefix must be a string'
        self.poke = poke
        self.feats = dict()
        self.battleFlag = isBattle
        self.prefix = prefix
        return
    
    #----------------------------------------------------------------------
    def applyprefix(self):
        new_feats = dict()
        if self.prefix:
            for (key, value) in self.feats.items():
                new_key = self.prefix + '_' + key
                new_feats[new_key] = value
            self.feats = new_feats
        return
    
    #----------------------------------------------------------------------
    def getFeats(self):
        self.applyprefix()
        return deepcopy(self.feats)
    
    #----------------------------------------------------------------------
    def extractNormStats(self):
        self.feats['Norm_HP'] = self.poke.Stats['HP']
        self.feats['Norm_Atk'] = self.poke.Stats['Atk']
        self.feats['Norm_Def'] = self.poke.Stats['Def']
        self.feats['Norm_SpA'] = self.poke.Stats['SpA']
        self.feats['Norm_SpD'] = self.poke.Stats['SpD']
        self.feats['Norm_Spe'] = self.poke.Stats['Spe']
        return
    
    #----------------------------------------------------------------------
    def extractBattleStats(self):
        #self.feats['Battle_HP'] = self.poke.b_stats['HP']
        #self.feats['Battle_Atk'] = self.poke.b_stats['Atk']
        #self.feats['Battle_Def'] = self.poke.b_stats['Def']
        #self.feats['Battle_SpA'] = self.poke.b_stats['SpA']
        #self.feats['Battle_SpD'] = self.poke.b_stats['SpD']
        #self.feats['Battle_Spe'] = self.poke.b_stats['Spe']
        self.feats['Battle_HP'] = self.poke.CurHP
        return
    
    #----------------------------------------------------------------------
    def extractNormMoveFeats(self):
        nMoves = self.poke.Moves.Nmovs
        for i, move in self.poke.Moves.Moves.items():
            # Get key root
            root = 'move_%i' %(i)
            
            # Get basic features
            acc = move.Accuracy
            power = move.Power
            
            self.feats[root+'_PP'] = move.PP
            if acc is None:
                self.feats[root+'_Acc'] = 100
            else:
                self.feats[root+'_Acc'] = move.Accuracy
            if power is None:
                self.feats[root+'_Power'] = 0
            else:
                self.feats[root+'_Power'] = move.Power
            
            # Get adjusted power feature
            if power is None:
                self.feats[root+'_adjPow'] = 0
            else:
                if move.Type in self.poke.Type:
                    stab = 1.5
                else:
                    stab = 1
                if move.Damage == 'physical':
                    dmg_stat = self.poke.Stats['Atk']
                elif move.Damage == 'special':
                    dmg_stat = self.poke.Stats['SpA']
                else:
                    dmg_stat = 0
                self.feats[root+'_adjPow'] = power*stab*dmg_stat        
        return
        
    #----------------------------------------------------------------------
    def extractBattleMoveFeats(self):
        nMoves = self.poke.Moves.Nmovs
        for i, move in self.poke.Moves.Moves.items():
            # Get key root
            root = 'move_%i' %(i)
            
            # Get battle specific features
            self.feats[root+'_CurPP'] = move.CurPP
        return
    
    #----------------------------------------------------------------------
    def extractTypeFeats(self):
        
        return
    
    #----------------------------------------------------------------------
    def extract(self):
        self.extractNormStats()
        self.extractNormMoveFeats()
        if self.battleFlag:
            self.extractBattleStats()
            self.extractBattleMoveFeats()
            
class teamExtractor:
    """Extracts features from a Team"""
    
    #----------------------------------------------------------------------
    def __init__(self, team, isBattle=False, prefix=''):
        """teamExtractor Constructor"""
        assert isinstance(team, pokeStructs.Team), 'Must be a team'
        assert isinstance(isBattle, bool), 'Battle Flag must be a boolean'
        assert isinstance(prefix, str), 'Key prefix must be a string'
        self.team = team
        self.feats = dict()
        self.battleFlag = isBattle
        self.prefix = prefix
        
    #----------------------------------------------------------------------
    def applyprefix(self):
        new_feats = dict()
        if self.prefix:
            for (key, value) in self.feats.items():
                new_key = self.prefix + '_' + key
                new_feats[new_key] = value
            self.feats = new_feats
        return
    
    #----------------------------------------------------------------------
    def getFeats(self):
        self.applyprefix()
        return deepcopy(self.feats)
    
    #----------------------------------------------------------------------
    def extractPokeFeats(self):
        for i in self.team.pos_taken():
            poke = self.team.get_Member(i)
            pkext = pokeExtractor(poke, self.battleFlag, str(i))
            pkext.extract()
            pk_feats = pkext.getFeats()
            self.feats.update(pk_feats)
        return
    
    #----------------------------------------------------------------------
    def extractTeamFeats(self):
        
        return
    
    #----------------------------------------------------------------------
    def extract(self):
        self.extractPokeFeats()