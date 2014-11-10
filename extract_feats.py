"""
togePy.extract_feats

This module extracts features of various togePy data structures.
"""
import pokeStructs
import save
import numpy as np
from copy import deepcopy
import os

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
        self.extractTeamFeats()
        return
    
class gameExtractor:
    """Extracts features from a Game"""
    
    #----------------------------------------------------------------------
    def __init__(self, game):
        """gameExtractor Constructor"""
        assert isinstance(game, pokeStructs.Game), 'Must be a game'
        self.game = game
        self.feats = dict()
        self.battleFlag = True
        if self.game.curActor is None:
            self.first = 'left'
        else:
            self.first = self.game.curActor
        
    #----------------------------------------------------------------------
    def getFeats(self):
        return deepcopy(self.feats)
    
    #----------------------------------------------------------------------
    def extractTeamFeats(self):
        if self.first == 'left':
            team1 = self.game.left.player.team
            team2 = self.game.right.player.team
        else:
            team1 = self.game.right.player.team
            team2 = self.game.left.player.team
            
        # Add team1's feats
        tmext = teamExtractor(team1, True, '1')
        tmext.extract()
        self.feats.update(tmext.getFeats())
        
        # Add team2's feats
        tmext = teamExtractor(team2, True, '2')
        tmext.extract()
        self.feats.update(tmext.getFeats())
        return
    
    #----------------------------------------------------------------------
    def extract(self):
        self.extractTeamFeats()
        return
        
########################################################################
class battleExtractor:
    """Iteratively gets updates to extract battle info"""

    #----------------------------------------------------------------------
    def __init__(self):
        """battleExtractor Constructor"""
        self.left = None
        self.right = None
        self.columns = None
        
    #----------------------------------------------------------------------
    def addFirstLine(self, raw_game):
        game = deepcopy(raw_game)
        game.curActor = 'left'
        gmext = gameExtractor(game)
        gmext.extract()
        feats = gmext.getFeats()
        items = feats.items()
        items.sort()
        vals = [v for (_, v) in items]
        line = np.array(vals)
        line = line.reshape((1, len(line)))
        self.left = line
        
        game.curActor = 'right'
        gmext = gameExtractor(game)
        gmext.extract()
        feats = gmext.getFeats()
        items = feats.items()
        items.sort()
        vals = [v for (_, v) in items]
        line = np.array(vals)
        line = line.reshape((1, len(line)))
        self.right = line
        
        self.columns = [k for (k, _) in items]
        
        return
        
    #----------------------------------------------------------------------
    def addLine(self, raw_game):
        assert isinstance(raw_game, pokeStructs.Game)
        game = deepcopy(raw_game)
        
        if game.curActor is None:
            self.addFirstLine(game)
        else:
            gmext = gameExtractor(game)
            gmext.extract()
            feats = gmext.getFeats()
            items = feats.items()
            items.sort()
            vals = [v for (_, v) in items]
            line = np.array(vals)
            line = line.reshape((1, len(line)))
            
            if game.curActor == 'left':
                self.left = np.concatenate((self.left, line), axis=0)
            elif game.curActor == 'right':
                self.right = np.concatenate((self.right, line), axis=0)
            else:
                assert False, 'Invalid Current Actor in Game'
        
        return
    
    #----------------------------------------------------------------------
    def addWinners(self, winner):
        l_rows = self.left.shape[0]
        r_rows = self.right.shape[0]
        l_dtype = self.left.dtype
        r_dtype = self.right.dtype
        
        if winner == 'left':
            l_col = np.ones((l_rows, 1), dtype=l_dtype)
            self.left = np.concatenate((self.left, l_col), axis=1)
            
            r_col = np.zeros((r_rows, 1), dtype=r_dtype)
            self.right = np.concatenate((self.right, r_col), axis=1)
        elif winner == 'right':
            l_col = np.zeros((r_rows, 1), dtype=r_dtype)
            self.right = np.concatenate((self.right, l_col), axis=1)
            
            r_col = np.ones((l_rows, 1), dtype=l_dtype)
            self.left = np.concatenate((self.left, r_col), axis=1)
        else:
            assert False, 'Invalid winner notation'
            
        return
    
    def writeData(self):
        complete = np.concatenate((self.left, self.right), axis=0)
        game_dir = save.create_game_dir()
        fname = os.path.join(game_dir, 'results.txt')
        np.savetxt(fname, complete, delimiter=',', fmt='%1.f')