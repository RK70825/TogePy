import battle
import pokeStructs
import pkmn_test
import save
import extract_feats
import random
import cPickle as pickle
from copy import deepcopy
import sys

def init_game():
    # Fake Battle Values
    battle_vals = dict()
    battle_vals['Level'] = 100
    battle_vals['# Poke'] = 6
    battle_vals['Items'] = True
    battle_vals['Tier'] = 'Uber'
    battle_vals['Players'] = 'CPU vs. CPU'
    
    # Initial teams. Random for now.
    team1 = pkmn_test.random_Team()
    team1.Name = 'Player 1'
    team2 = pkmn_test.random_Team()
    team2.Name = 'Player 2'
    
    # Prep Teams for Battle
    team1.init_battle(battle_vals)
    team2.init_battle(battle_vals)
    
    # Location for where battle_vals['# Poke'] will be respected
    
    # Initialize Players
    player1 = pokeStructs.Player('CPU', team1)
    player2 = pokeStructs.Player('CPU', team2)
    
    # Initialize Fields
    left_field = pokeStructs.Field()
    right_field = pokeStructs.Field()
    main_field = pokeStructs.Field()    
    
    # Initialize Sides
    left = pokeStructs.Side(player1, left_field)
    right = pokeStructs.Side(player2, right_field)
    
    # Initialize Game
    game = pokeStructs.Game(left, right, main_field)
    
    return game

def pkstr(poke):
    return '%s[%i/%i]' %(poke.Name, poke.CurHP, poke.Stats['HP'])

def pick_poke(player):
    # Grab Team Health Status
    team = player.team
    fainted = team.battle_ready()
    
    # Get random choice
    choices = fainted.items()
    live = [(i, f) for i, f in choices if f == 'A']
    opt = random.choice(live)
    ind = opt[0]
    
    return ind

def get_action(user, receiver):
    def greedy(user, receiver):
        # Looks at move with highest damage
        atker = user.poke
        recvr = receiver.poke
        moves = atker.Moves.Moves
        max_dmg = -1
        
        for m in range(1, 5):
            if moves[m].CurPP > 0:
                try:
                    dmg = battle.calc_Damage(atker, recvr, moves[m])
                except:
                    dmg = 0
                if dmg > max_dmg:
                    max_dmg = dmg
                    choice = ('move', m)
        
        return choice
    
    choice = greedy(user, receiver)
    
    return choice

def get_turn_order(choice1, choice2, player1, player2):
    # Get Move Priorities
    pr1 = battle.turn_priority(choice1)
    pr2 = battle.turn_priority(choice2)
    
    # Compare Priorities
    if pr1 < pr2:
        first = 1
    elif pr2 < pr1:
        first = 2
    else:
        first = battle.compare_speed(player1.poke, player2.poke)
    
    return first

def execute_choice(choice, user, receiver, verbose):
    if choice[0] == 'switch':
        user.poke = user.team.get_Member(choice[1])
    elif choice[0] == 'move':
        # Get and Write move Info
        atker = user.poke
        recvr = receiver.poke
        move = user.poke.Moves.Moves[choice[1]]
        if verbose:
            print '%s used %s' %(pkstr(atker), move.Name)
        move.CurPP -= 1
        
        # Calculate Damage
        try:
            dmg = battle.calc_Damage(atker, recvr, move)
        except:
            dmg = 0
        
        # Check Accuracy
        if battle.acc_check(move):
            recvr.mod_HP(-1*dmg)
            if verbose:
                print '%s took %i damage' %(pkstr(recvr), dmg)
                if recvr.CurHP == 0:
                    print '%s fainted' %(recvr.Name)
        else:
            if verbose:
                print 'The attack missed'
                
    return

def check_gameover(player1, player2):
    f1 = player1.team.battle_ready()
    n1 = sum([1 if (f1[k] == 'A') else 0 for k in f1.keys()])
    f2 = player2.team.battle_ready()
    n2 = sum([1 if (f2[k] == 'A') else 0 for k in f2.keys()])
    if (n1 == 0) or (n2 == 0):
        return True
    else:
        return False
    
def check_winner(player1, player2):
    if check_gameover(player1, player1):
        return 2
    else:
        return 1

def auto(game, verbose, fext):
    # Prepare game
    player1 = game.left.player
    player2 = game.right.player
    game.curActor = 'left'
    player1.poke = player1.team.get_Member(pick_poke(player1))
    game.curActor = 'right'
    player2.poke = player2.team.get_Member(pick_poke(player2))
    if verbose:
        print '%s sent out %s' %(player1.team.Name, pkstr(player1.poke))
        print '%s sent out %s\n' %(player2.team.Name, pkstr(player2.poke))
    if fext:
        btext = extract_feats.battleExtractor()
        btext.addFirstLine(game)
    
    while True:
        # Get Player Choices and Order
        game.curActor = 'left'
        p1_choice = get_action(player1, player2)
        game.curActor = 'right'
        p2_choice = get_action(player2, player1)
        first_player = get_turn_order(p1_choice, p2_choice, player1, player2)
        
        # Get Choice Order
        if first_player == 1:
            p1 = player1
            p2 = player2
            first_choice = p1_choice
            second_choice = p2_choice
            first_actor = 'left'
            second_actor = 'right'
        else:
            p1 = player2
            p2 = player1
            first_choice = p2_choice
            second_choice = p1_choice
            first_actor = 'right'
            second_actor = 'left'
            
        # Execute Choices
        execute_choice(first_choice, p1, p2, verbose)
        game.curActor = first_actor
        if game.logging:
            save.save_Game(game)
        if fext:
            btext.addLine(game)
        if check_gameover(p1, p2):
            break
        elif p2.poke.CurHP == 0:
            p2.poke = p2.team.get_Member(pick_poke(p2))
            game.curActor = second_actor
            if verbose:
                print '%s sent out %s' %(p2.team.Name, pkstr(p2.poke))
            if game.logging:
                save.save_Game(game)
            if fext:
                btext.addLine(game)
        else:
            execute_choice(second_choice, p2, p1, verbose)
            game.curActor = second_actor
        if game.logging:
            save.save_Game(game)
        if fext:
            btext.addLine(game)
        
        if check_gameover(p1, p2):
            break
        elif p1.poke.CurHP == 0:
            p1.poke = p1.team.get_Member(pick_poke(p1))
            game.curActor = first_actor
            if verbose:
                print '%s sent out %s' %(p1.team.Name, pkstr(p1.poke))
            if game.logging:
                save.save_Game(game)
            if fext:
                btext.addLine(game)
                
        # Separate Turns
        if verbose:
            print ''
    
    if check_winner(player1, player2) == 1:
        winner = player1.team.Name
        fextwin = 'left'
    else:
        winner = player2.team.Name
        fextwin = 'right'
    
            
    if verbose:
        win_string = '###%s has won the game!###' %(winner)
        print '\n'+'#'*len(win_string)
        print win_string
        print '#'*len(win_string)
    if fext:
        btext.addLine(game)
        btext.addWinners(fextwin)
        btext.writeData()
        
    return

def main(verbose=False, logging=False, fext=False):
    game = init_game()
    if logging:
        game.init_logging()
    auto(game, verbose, fext)
    return

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(bool(int(sys.argv[1])))
    elif len(sys.argv) == 3:
        main(bool(int(sys.argv[1])), bool(int(sys.argv[2])))
    elif len(sys.argv) == 4:
        main(bool(int(sys.argv[1])), bool(int(sys.argv[2])), bool(int(sys.argv[3])))
    else:
        main()