import curses
import pkmn_test
from pkmn_test import pokeStructs
import numpy as np
import save
from copy import deepcopy
import sys
import time
import random
import battle

screen = curses.initscr()
screen.clear()
screen.refresh()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
curses.start_color()
dims = screen.getmaxyx()

def intro():
    lines = [
    '',
    '              ?::           MM          ',
    '             M::::M ~~M  ::::           ',
    '         $N  :::::::~~D:::::7           ',
    '         ~~~M:::::::::::::::            ',
    '    :::::::7::::::7:::::::::            ',
    '     ~:::::::::,D?O::::::::M            ',
    '      7~:::::::::II:::::::::            ',
    '       N~~::::::N:::? :::~:   D         ',
    '        M+    $        ~::::O           ',
    '    ~::D    Z           O~~:M  M        ',
    '     ~~~::                              ',
    '      M~~~     IIIIIII      MIIZ        ',
    '      M::       I:    I.  I:::::M       ',
    '       :~OZZ     I+   7  M:~~~~~:       ',
    '       MOO:OZZ    ?III   :~~~~~~D       ',
    '        M+::,OZ        :O~~~~~~~        ',
    '          :::OOO::.  III~~Z777?M        ',
    '            8O::::::::77Z~~~~~M         ',
    '           M:::~8Z=~$M    MM            ',
    '          :::::~~~~~                    ',
    '',
    'TogePy',
    '2014 - Ross Kleiman'
    ]
    for z, l in enumerate(lines):
        screen.addstr((dims[0] - len(lines))/2 + z, (dims[1] - len(l))/2, l)
    screen.refresh()
    key = screen.getch()
    if key == ord('q'):
        screen.clear()
        screen.refresh()
        sys.exit()
    else:
        return
    
def menu():
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    lines = ['Debug', 'Build', 'Train', 'Battle', 'Exit']
    while selection < 0:
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        title = 'TogePy'
        screen.addstr(0, (dims[1] - len(title))/2, title) #Show Title
        for i, l in enumerate(lines):
            screen.addstr((dims[0] - len(lines))/2 + i, (dims[1] - len(l))/2, l, graphics[i])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == ord('\n'):
            selection = option
        elif action == ord('q'):
            selection = action
        screen.refresh()
    screen.clear()
    if selection == 0:
        debug()
    elif selection == 1:
        build_menu()
    elif selection == 2:
        under_Construction()
        menu()
    elif selection == 3:
        battle_menu()
    else:
        return

def debug():
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    lines = ['Rand Team', 'Rand Poke', 'Rand Move', 'Rand Item', 'Rand Ability', 'Exit']
    while selection < 0:
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        title = 'TogePy'
        screen.addstr(0, (dims[1] - len(title))/2, title) #Show Title
        for i, l in enumerate(lines):
            screen.addstr((dims[0] - len(lines))/2 + i, (dims[1] - len(l))/2, l, graphics[i])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == ord('\n'):
            selection = option
        elif action == ord('q'):
            selection = action
        screen.refresh()
    screen.clear()
    if selection == 0:
        d_team(pkmn_test.random_Team())
        debug()
    elif selection == 1:
        d_poke(pkmn_test.random_Poke())
        debug()
    elif 2 <= selection <= 4:
        under_Construction()
        debug()
    else:
        menu()
        
def d_team(team):
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    while selection < 0:
        screen.border()
        tName = 'Team: '+team.Name
        screen.addstr(1, (dims[1] - len(tName))/2, tName, curses.A_BOLD)
        graphics = [0]*team.Nmems
        graphics[option] = curses.A_BLINK
        for i in xrange(1, team.Nmems + 1):
            pk = team.get_Member(i)
            Name = pk.Name
            if len(Name) > 13:
                d_Name = Name[0:10]+'...'
            else:
                d_Name = Name
            screen.addstr(3*i+2, 1, d_Name, curses.A_BOLD | graphics[i - 1])
            screen.addstr(3*i+2, 17, 'Lv. '+str(int(pk.Level)).rjust(3, ' '))
            max_HP = pk.Stats['HP']
            cur_HP = pk.CurHP
            s_hp = 'HP: '+str(int(cur_HP)).rjust(3,' ')+'/'+str(int(max_HP)).ljust(3,' ')
            x = np.ceil(cur_HP * 20. / max_HP)
            screen.addstr(3*i+2, 27, s_hp)
            screen.addstr(3*i+2, 39, '['+('X'*x).ljust(20, ' ')+']')
            Item = str(pk.Item)
            sts = str(pk.Status)
            if sts == 'None':
                sts = '---'
            if len(Item) > 0:
                hasItem = 1
            else:
                hasItem = 0
            screen.addstr(3*i+2, 64, 'Item: ['+('X'*hasItem).ljust(1,' ')+']')
            d_status = {'---':0, 'PSN':1, 'BRN':2, 'FZN':3, 'SLP':4, 'PAR':5}
            curses.init_color(15, 500, 500, 500)
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(4, curses.COLOR_WHITE, 8)
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_YELLOW)
            screen.addstr(3*i+2, 76, sts, curses.color_pair(d_status[sts]))
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%team.Nmems
        elif action == curses.KEY_DOWN:
            option = (option + 1)%team.Nmems
        elif action == ord('\n'):
            selection = option
        elif action == ord('q'):
            selection = action
    if selection == ord('q'):
        return
    else:
        pk = team.get_Member(selection + 1)
        d_poke(pk)
        d_team(team)
    screen.clear()

def d_poke(pk):
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    while selection < 0:
        screen.border()
        screen.addstr(1, (dims[1] - len(pk.Name))/2, pk.Name, curses.A_BOLD)
        screen.addstr(2, (dims[1] - 6)/2, 'Lv. '+str(int(pk.Level)).ljust(3, ' '))
        max_HP = pk.Stats['HP']
        cur_HP = pk.CurHP
        s_hp = 'HP: '+str(int(cur_HP)).rjust(3,' ')+'/'+str(int(max_HP)).ljust(3,' ')
        n = float(dims[1]-16)
        x = np.ceil(cur_HP * n / max_HP)
        screen.addstr(5, 1, s_hp)
        screen.addstr(5, 13, '['+('X'*x).ljust(int(n), ' ')+']')
        stats = {0:'HP', 1:'Atk', 2:'Def', 3:'SpA', 4:'SpD', 5:'Spe'}
        vals = {0:' Stats ', 1:'  EVs  ', 2:'  IVs  '}
        for i in xrange(6):
            screen.vline(8, 6*i+9, 0, 7)
            screen.addstr(8, 6*i+10, stats[i].center(5))
            screen.addstr(10, 6*i+10, str(int(pk.Stats[stats[i]])).center(5))
            screen.addstr(12, 6*i+10, str(int(pk.EVs[stats[i]])).center(5))
            screen.addstr(14, 6*i+10, str(int(pk.IVs[stats[i]])).center(5))
        for i in xrange(3):
            screen.hline(2*i+9, 2, 0, 43)
            screen.addstr(2*i+10, 2, vals[i])
        t = ''
        for x in pk.Type:
            t += x.capitalize()+'/'
        t = t[:-1]
        screen.addstr(8, 50, 'Type: '+t)
        screen.addstr(10, 50, 'Ability: '+pk.Ability.capitalize())
        screen.addstr(12, 50, 'Nature: '+pk.NatureName)
        screen.addstr(14, 50, 'Item: '+str(pk.Item))
        for i in xrange(2):
            for j in xrange(2):
                m_Num = 2*j+i+1
                move = pk.Moves.Moves[m_Num]
                m_Name = move.Name
                m_PP = str(move.CurPP)+'/'+str(move.PP)
                m_Type = move.Type
                m_Dmg = move.Damage.capitalize()
                if move.Power == None:
                    m_Pwr = 'PWR: -'
                else:
                    m_Pwr = 'PWR: '+str(int(move.Power))
                if move.Accuracy == None:
                    m_Acc = 'ACC: -'
                else:
                    m_Acc = 'ACC: '+str(int(move.Accuracy))
                r1 = m_Name+' - '+m_PP
                r2 = m_Type+' - '+m_Dmg
                r3 = m_Pwr+' - '+m_Acc
                screen.addstr(16+4*j, (2*i+1)*dims[1]/4-len(r1)/2, r1)
                screen.addstr(17+4*j, (2*i+1)*dims[1]/4-len(r2)/2, r2)
                screen.addstr(18+4*j, (2*i+1)*dims[1]/4-len(r3)/2, r3)
        screen.refresh()
        selection = screen.getch()
    screen.clear()
    
def build_menu():
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    lines = ['Build Poke', 'Build Team', 'Exit']
    while selection < 0:
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        title = 'TogePy'
        screen.addstr(0, (dims[1] - len(title))/2, title) #Show Title
        for i, l in enumerate(lines):
            screen.addstr((dims[0] - len(lines))/2 + i, (dims[1] - len(l))/2, l, graphics[i])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == ord('\n'):
            selection = option
        elif action == ord('q'):
            selection = action
        screen.refresh()
    screen.clear()
    if selection == 0:
        "Build Poke"
        build_poke()
    elif selection == 1:
        "Build Team"
        build_team()
    else:
        menu()
        
def build_poke():
    screen.nodelay(0)
    screen.clear()
    dex = pkmn_test.pokedex
    pk = [(x, dex[x].Name) for x in dex.keys()]
    pk.sort()
    levels = dict(zip(range(100), range(1, 101)))
    natures = dict(zip(range(25),pkmn_test.nature_list()))
    items = pkmn_test.items.keys()
    items.sort()
    items = ['None'] + items
    moves = pkmn_test.moves.keys()
    moves.sort()
    moves = ['None'] + moves
    selection = -1
    option = 0
    ev_op = 0
    iv_op = 0
    lines = ['Pokemon', 'Level', 'Nature', 'Happiness', 'EVs', 'IVs', 'Ability', 'Item', 'Move_1', 'Move_2', 'Move_3', 'Move_4', 'Save']
    #Create dictionaries needed to support selections
    vals = dict(zip(range(len(lines)), [0]*len(lines)))
    ev_vals = dict(zip(range(6), [0]*6))
    iv_vals = dict(zip(range(6), [0]*6))
    strvals = dict(zip(range(len(lines)), ['']*len(lines)))
    maxval = dict(zip(range(len(lines)), [1]*len(lines)))
    #Set max unique values for each option
    maxval[0] = len(pk)
    maxval[1] = 100
    maxval[2] = len(natures)
    maxval[3] = 256
    maxval[4] = 256
    maxval[5] = 32
    maxval[7] = len(items)
    maxval[8] = len(moves)
    maxval[9] = len(moves)
    maxval[10] = len(moves)
    maxval[11] = len(moves)
    #Display stuff
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    while selection < 0:
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        ev_graphics = [0]*6
        ev_graphics[ev_op] = curses.A_BOLD
        iv_graphics = [0]*6
        iv_graphics[iv_op] = curses.A_BOLD
        screen.clear()
        screen.border()
        # Display Options
        for i, l in enumerate(lines):
            screen.addstr(i+1, 1, l, graphics[i])
        # Update string values for each option
        strvals[0] = '[' + str(pk[vals[0]][0]).rjust(3,'0') + '] ' + pk[vals[0]][1]
        strvals[1] = str(levels[vals[1]])
        strvals[2] = str(natures[vals[2]])
        strvals[3] = str(vals[3])
        abils = dex[vals[0]+1].Abilities
        abils.sort()
        maxval[6] = len(abils)
        if (vals[6]+1) > maxval[6]:
            vals[6] = 0
        strvals[6] = abils[vals[6]]
        strvals[7] = items[vals[7]]
        strvals[8] = moves[vals[8]]
        strvals[9] = moves[vals[9]]
        strvals[10] = moves[vals[10]]
        strvals[11] = moves[vals[11]]
        # Display Values for each option
        for i in range(len(lines)):
            screen.addstr(i+1, len(lines[i])+2, strvals[i])
        for i, s in enumerate([' HP: ', 'Atk: ', 'Def: ', 'SpA: ', 'SpD', 'Spe: ']):
            screen.addstr(5, 9*i+4, s, ev_graphics[i])
            screen.addstr(6, 9*i+4, s, iv_graphics[i])
            screen.addstr(5, 9*i+9, str(ev_vals[i]).rjust(3,' '))
            screen.addstr(6, 9*i+9, str(iv_vals[i]).rjust(3,' '))
        # Create Pokemon
        p_dex = dex[vals[0]+1]
        lvl = levels[vals[1]]
        EVs = pokeStructs.createEVs(ev_vals)
        IVs = pokeStructs.createIVs(iv_vals)
        Nature = natures[vals[2]]
        Happiness = vals[3]
        Ability = abils[vals[6]]
        moveset = pokeStructs.Moveset()
        for i in xrange(1, 5):
            m = strvals[i + 7]
            if m != 'None':
                moveset.set_Move(i, pkmn_test.moves[m])
        if strvals[7] != 'None':
            Item = items[vals[7]]
        else:
            Item = False
        poke = pokeStructs.Pokemon(p_dex, lvl, EVs, IVs, Nature, Happiness, Ability, moveset, Item)
        # Display Pokemon Stats
        for i, s in enumerate(['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']):
            if poke.Nature[s] < 1.0:
                col = curses.color_pair(2)
            elif poke.Nature[s] > 1.0:
                col = curses.color_pair(3)
            else:
                col = curses.color_pair(0)
            screen.addstr(18, 9*i+11, s.rjust(3,' ')+': ')
            screen.addstr(18, 9*i+16, str(int(poke.Stats[s])).rjust(3,' '), col)
        # Handle user input selection
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_LEFT:
            if option == 4: #Special handling for EV
                if ev_vals[ev_op] == 0 and sum(ev_vals.values()) + 255 <= 510:
                    ev_vals[ev_op] = (ev_vals[ev_op] - 1)%maxval[option]
                elif ev_vals[ev_op] != 0:
                    ev_vals[ev_op] = (ev_vals[ev_op] - 1)%maxval[option]
            elif option == 5: #Special handling for IV
                iv_vals[iv_op] = (iv_vals[iv_op] - 1)%maxval[option]
            else:
                vals[option] = (vals[option]-1)%maxval[option]
        elif action == curses.KEY_RIGHT:
            if option == 4: #Special handling for EV
                if sum(ev_vals.values()) < 510:
                    ev_vals[ev_op] = (ev_vals[ev_op] + 1)%maxval[option]
                elif sum(ev_vals.values()) == 510 and ev_vals[ev_op] == 255:
                    ev_vals[ev_op] = (ev_vals[ev_op] + 1)%maxval[option]
            elif option == 5: #Special handling for IV
                iv_vals[iv_op] = (iv_vals[iv_op] + 1)%maxval[option]
            else:
                vals[option] = (vals[option]+1)%maxval[option]
        elif action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == 351: #SHIFT-TAB
            if option == 4:
                ev_op = (ev_op - 1)%6
            elif option == 5:
                iv_op = (iv_op - 1)%6
        elif action == 9: #TAB
            if option == 4:
                ev_op = (ev_op + 1)%6
            elif option == 5:
                iv_op = (iv_op + 1)%6
        elif action == ord('\n') and option == 12:
            selection = 'save'
        elif action == ord('q'):
            selection = action
        elif action == ord('d'):
            d_poke(poke)
        screen.refresh()
    if selection == 'save':
        save.save_Poke(poke)
    screen.clear()
    build_menu()
    
def build_team():
    screen.nodelay(0)
    screen.clear()
    pk = ['None'] + save.get_Files('POKE')
    selection = -1
    option = 0
    lines = ['Member_1', 'Member_2', 'Member_3', 'Member_4', 'Member_5', 'Member_6', 'Team Name', 'Save']
    #Create dictionaries needed to support selections
    vals = dict(zip(range(len(lines)), [0]*len(lines)))
    strvals = dict(zip(range(len(lines)), ['']*len(lines)))
    maxval = dict(zip(range(len(lines)), [1]*len(lines)))
    #Set max unique values for each option
    maxval[0:6] = [len(pk)]*6
    while selection < 0:
        # Display Static Information
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        screen.clear()
        for i, l in enumerate(lines):
            screen.addstr(i+1, 1, l, graphics[i])        
        screen.border()
        # Update string values for each option
        for i in range(6):
            strvals[i] = pk[vals[i]]
        # Display Current Choices
        for i in range(len(lines)):
            screen.addstr(i+1, len(lines[i])+2, strvals[i])
        # Flush to Screne        
        screen.refresh()
        # Create Pokemon and team
        if strvals[6] == '':
            tName = 'Unnamed Team'
        else:
            tName = strvals[6]
        team = pokeStructs.Team(tName)
        for i in range(6):
            if strvals[i] != 'None':
                poke = save.load_Poke(strvals[i])
                team.set_Member(i+1, poke)
        # Key Stuff
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == curses.KEY_LEFT:
            vals[option] = (vals[option]-1)%maxval[option]
        elif action == curses.KEY_RIGHT:
            vals[option] = (vals[option]+1)%maxval[option]
        elif action == ord('\n'):
            if option in range(6):
                poke = team.get_Member(option+1)
                if poke != 'Position Empty':
                    d_poke(poke)
            elif option == 6:
                curses.echo()
                screen.addstr(7, 11, '?')
                strvals[6] = screen.getstr(7, 11)
                curses.noecho()
                screen.getch()
            elif option == 7:
                save.save_Team(team)
                selection = action
        elif action == ord('q'):
            selection = action
        elif action == ord('d'):
            d_team(team)
        screen.refresh()
    screen.clear()
    build_menu()
    
def battle_menu():
    lines = ['Single', 'Double', 'Triple', 'Rotation', 'Exit']
    selection = standard_menu(lines)
    if selection in range(4):
        battle_opts = dict()
        battle_opts['# Poke'] = [6, 1, 2, 3, 4, 5]
        battle_opts['Items'] = [True, False]
        battle_opts['Tier'] = ['Uber', 'Overused', 'Borderline', 'Underused', 'Borderline 2', 'Rarelyused', 'Neverused', 'Little Cup', 'Limbo', 'Not Fully Evolved']
        battle_opts['Level'] = ['As Is', 50, 100]
        battle_opts['Players'] = ['Human vs. CPU', 'CPU vs. CPU', 'Human vs. Human']
        battle_vals = user_options(battle_opts, 'Battle Options')
        if battle_vals['Players'] == 'Human vs. CPU':
            p1_type = 'Human'
            p2_type = 'CPU'
            team1 = deepcopy(select_team('Player 1'))
            team2 = deepcopy(pkmn_test.random_Team())
        elif battle_vals['Players'] == 'CPU vs. CPU':
            p1_type = 'CPU'
            p2_type = 'CPU'
            team1 = deepcopy(pkmn_test.random_Team())
            team2 = deepcopy(pkmn_test.random_Team())
        elif battle_vals['Players'] == 'Human vs. Human':
            p1_type = 'Human'
            p2_type = 'Human'
            team1 = deepcopy(select_team('Player 1'))
            team2 = deepcopy(select_team('Player 2'))
        else:
            sys.exit(1234)
        team1.init_battle(battle_vals)
        team2.init_battle(battle_vals)
        if int(battle_vals['# Poke']) == 6:
            t1_members = dict(zip(range(6), [1]*6))
            t2_members = dict(zip(range(6), [1]*6))
        else:
            t1_members = select_poke(team1, int(battle_vals['# Poke']))
            t2_members = select_poke(team2, int(battle_vals['# Poke']))
        team1_battle = pokeStructs.Team(team1.Name)
        team1_battle.set_All([team1.get_Member(i+1) for i in t1_members.keys() if t1_members[i] == 1])
        team2_battle = pokeStructs.Team(team2.Name)
        team2_battle.set_All([team2.get_Member(i+1) for i in t2_members.keys() if t2_members[i] == 1])
        player_1 = pokeStructs.Player(p1_type, team1_battle)
        player_2 = pokeStructs.Player(p2_type, team2_battle)
        #d_team(team1)
        #d_team(team2)
        battle_screen(player_1, player_2)
    else:
        menu()
        
def battle_screen(player_1, player_2):
    def turn_setup():
        screen.nodelay(0)
        screen.clear()
        box2.clear()
        screen.border()
        d_eevee(6, 6)
        d_eevee(1, 55)
        box1.box()
        box2.box()
        p1_box.box()
        p2_box.box()
        d_battle_pokes(player_1.poke, player_2.poke)
        screen.refresh()
        box1.refresh()
        box2.refresh()
        p1_box.refresh()
        p2_box.refresh()
        
    def turn_breakdown():
        screen.refresh()
        box1.refresh()
        box2.refresh()
        p1_box.refresh()
        p2_box.refresh()
        return
    
    def pick_poke(player, can_quit=False):
        team = player.team
        fainted = team.battle_ready()
        def human_choice():
            poke_win = curses.newwin(25, 80, 0, 0)
            selection = -1
            option = 0
            while selection < 0:
                graphics = [0]*team.Nmems
                graphics[option] = curses.A_BLINK
                poke_win.clear()
                poke_win.box()
                tName = 'Team: '+team.Name
                poke_win.addstr(1, (dims[1] - len(tName))/2, tName, curses.A_BOLD)
                for i in xrange(1, team.Nmems + 1):
                    pk = team.get_Member(i)
                    Name = pk.Name
                    if len(Name) > 13:
                        d_Name = Name[0:10]+'...'
                    else:
                        d_Name = Name
                    poke_win.addstr(3*i+2, 1, d_Name, curses.A_BOLD | graphics[i - 1])
                    poke_win.addstr(3*i+2, 17, 'Lv. '+str(int(pk.Level)).rjust(3, ' '))
                    max_HP = pk.Stats['HP']
                    cur_HP = pk.CurHP
                    s_hp = 'HP: '+str(int(cur_HP)).rjust(3,' ')+'/'+str(int(max_HP)).ljust(3,' ')
                    x = np.ceil(cur_HP * 20. / max_HP)
                    poke_win.addstr(3*i+2, 27, s_hp)
                    poke_win.addstr(3*i+2, 39, '['+('X'*x).ljust(20, ' ')+']')
                    Item = str(pk.Item)
                    sts = str(pk.Status)
                    if sts == 'None':
                        sts = '---'
                    if len(Item) > 0:
                        hasItem = 1
                    else:
                        hasItem = 0
                    poke_win.addstr(3*i+2, 64, 'Item: ['+('X'*hasItem).ljust(1,' ')+']')
                    d_status = {'---':0, 'PSN':1, 'BRN':2, 'FZN':3, 'SLP':4, 'PAR':5}
                    curses.init_color(15, 500, 500, 500)
                    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
                    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
                    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
                    curses.init_pair(4, curses.COLOR_WHITE, 8)
                    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_YELLOW)
                    poke_win.addstr(3*i+2, 76, sts, curses.color_pair(d_status[sts]))
                screen.refresh()
                poke_win.refresh()
                action = screen.getch()
                if action == curses.KEY_UP:
                    option = (option - 1)%team.Nmems
                elif action == curses.KEY_DOWN:
                    option = (option + 1)%team.Nmems
                elif action == ord('d'):
                    d_poke(team.get_Member(option+1))
                    poke_win.touchwin()
                    poke_win.refresh()
                elif action == ord('\n'):
                    if fainted[option+1] == 'F':
                        invalid_option()
                        poke_win.touchwin()
                        poke_win.refresh()
                    else:
                        selection = option
                elif action in [ord('q'), ord('b')]:
                    if can_quit:
                        selection = 'b'
                    else:
                        invalid_option()
                        poke_win.touchwin()
                        poke_win.refresh()
            if selection == 'b':
                poke_win.clear()
                poke_win.refresh()
                del poke_win
                screen.refresh()
                return 'b'
            elif selection == ord('d'):
                pk = team.get_Member(selection + 1)
                d_poke(pk)
            poke_win.clear()
            del poke_win
            return selection+1
        
        def cpu_choice():
            while True:
                i = random.choice(fainted.keys())
                if fainted[i] == 'A':
                    break
            return i
        
        if player.p_Type == 'Human':
            return human_choice()
        elif player.p_Type == 'CPU':
            return cpu_choice()
        
    def get_choices():
        def human_choice(player):
            q = False
            Select = False
            while Select == False:
                act_1 = get_action_1()
                if act_1 in ['q', 3]:
                    choice = 'q'
                    q = True
                elif act_1 == 1:
                    choice = 'b'
                    invalid_option()
                elif act_1 == 0:
                    choice = get_move(player.poke)
                elif act_1 == 2:
                    choice = ('switch', pick_poke(player, True))
                    if choice[1] == 'b':
                        choice = 'b'
                
                if choice == 'b':
                    box2.clear()
                    box2.box()
                    box2.refresh()
                    continue
                elif choice == 'q':
                    Select = True
                    q = True
                else:
                    Select = True
            
            return q, choice
        
        def cpu_choice(player):
            moves = player.poke.Moves.Moves
            m_Num = random.choice(range(1, 5))
            choice = ('move', m_Num)
            return choice
        
        q = False
        
        if player_1.p_Type == 'Human':
            q, p1_choice = human_choice(player_1)
        elif player_1.p_Type == 'CPU':
            p1_choice = cpu_choice(player_1)
            
        box2.clear()
        box2.box()
        box2.refresh()
        
        if player_2.p_Type == 'Human':
            q, p2_choice = human_choice(player_2)
        elif player_2.p_Type == 'CPU':
            p2_choice = cpu_choice(player_2)
            
        return p1_choice, p2_choice, q
        
    def get_action_1():
        box1_row = 0
        box1_col = 0
        box1_lines = ['Fight', '---', 'Pokemon', 'Run']
        selection = -1
        
        while selection < 0:
            box1_option = 2*box1_col + box1_row
            box1_graphics = [0]*4
            box1_graphics[box1_option] = curses.A_REVERSE
            box1.clear()
            box1.box()
            box1.addstr(2, 2, box1_lines[0], box1_graphics[0])
            box1.addstr(2, 12, box1_lines[1], box1_graphics[1])
            box1.addstr(4, 2, box1_lines[2], box1_graphics[2])
            box1.addstr(4, 12, box1_lines[3], box1_graphics[3])
            box1.refresh()
            
            action = screen.getch()
            if action == curses.KEY_UP:
                box1_col = (box1_col - 1)%2
            elif action == curses.KEY_DOWN:
                box1_col = (box1_col + 1)%2
            elif action == curses.KEY_LEFT:
                box1_row = (box1_row - 1)%2
            elif action == curses.KEY_RIGHT:
                box1_row = (box1_row + 1)%2
            elif action == ord('q'):
                selection = 'q'
            elif action == ord('\n'):
                selection = box1_option
            elif action == curses.KEY_MOUSE:
                box1_col = (box1_col - 1)%2
            else:
                continue
        return selection
    
    def get_move(poke):
        box2_row = 0
        box2_col = 0
        r1 = {}
        r2 = {}
        selection = -1
        moves = poke.Moves.Moves        
        for i in xrange(2):
            for j in xrange(2):
                m_Num = 2*j+i+1
                move = moves[m_Num]
                m_Name = move.Name
                m_PP = str(move.CurPP)+'/'+str(move.PP)
                m_Type = move.Type
                m_Dmg = move.Damage.capitalize()
                if move.Power == None:
                    m_Pwr = 'PWR: -'
                else:
                    m_Pwr = 'PWR: '+str(int(move.Power))
                if move.Accuracy == None:
                    m_Acc = 'ACC: -'
                else:
                    m_Acc = 'ACC: '+str(int(move.Accuracy))
                r1[m_Num-1] = m_Name+' - '+m_PP
                r2[m_Num-1] = m_Type+' - '+m_Dmg
        
        while selection < 0:
            box2_option = 2*box2_col + box2_row
            box2_graphics = [0]*4
            box2_graphics[box2_option] = curses.A_REVERSE
            box2.clear()
            box2.box()
            for m_Num in range(4):
                i = m_Num%2
                j = m_Num/2
                s1 = r1[m_Num]
                s2 = r2[m_Num]
                box2.addstr(1+3*j, (2*i+1)*box2_dims[1]/4-len(s1)/2, s1, box2_graphics[m_Num])
                box2.addstr(2+3*j, (2*i+1)*box2_dims[1]/4-len(s2)/2, s2, box2_graphics[m_Num])
            box2.refresh()
            
            action = screen.getch()
            if action == curses.KEY_UP:
                box2_col = (box2_col - 1)%2
            elif action == curses.KEY_DOWN:
                box2_col = (box2_col + 1)%2
            elif action == curses.KEY_LEFT:
                box2_row = (box2_row - 1)%2
            elif action == curses.KEY_RIGHT:
                box2_row = (box2_row + 1)%2
            elif action == ord('q'):
                return 'q'
            elif action == ord('b'):
                return 'b'
            elif action == ord('\n'):
                selection = box2_option
            else:
                continue
        return ('move', selection+1)
    
    def d_battle_pokes(pk1, pk2):
        def pk_lines(pk):
            name = pk.Name
            lv = str(int(pk.Level))
            cur_hp = int(pk.CurHP)
            max_hp = int(pk.Stats['HP'])
            
            ws_1 = 24 - (len(name) + len(lv) + 2)
            line1 = name + ' '*ws_1 + 'Lv' + lv
            n_x = np.ceil(15 * cur_hp / max_hp)
            line2 = ' '*5 + 'HP[' + 'X'*n_x + ' '*(15-n_x) + ']'
            line3 = str(cur_hp) + '/' + str(max_hp)
            line3 = line3.rjust(24)
            lines = [line1, line2, line3]
            return lines
        
        def print_poke(box, lines):
            box.addstr(1, 1, lines[0])
            box.addstr(2, 1, lines[1])
            box.addstr(3, 1, lines[2])
        
        lines_1 = pk_lines(pk1)
        lines_2 = pk_lines(pk2)
        print_poke(p1_box, lines_1)
        print_poke(p2_box, lines_2)
        
        return
    
    def d_eevee(y, x):
        eevee = [';-.               ,',
                 ' \ \'.           .\'/',
                 '  \  \ .---. .-\' / ',
                 '   \'. \'     `\_.\'  ',
                 '     |(),()  |     ,',
                 '     (  __   /   .\' \\',
                 '    .\'\'.___.\'--,/\_,|',
                 '   {  /     \   }   |',
                 '    \'.\     /_.\'    /',
                 '     |\'-.-\',  `; _.\'',
                 '     |  |  |   |`',
                 '     `""`""`"""`  ']
        
        for i in range(len(eevee)):
            screen.addstr(y + i, x, eevee[i])
        
    def invalid_option():
        inv_win = curses.newwin(3, 20, 11, 30)
        inv_win.box()
        inv_win.addstr(1, 1, 'Invalid  Selection')
        screen.refresh()
        inv_win.refresh()
        inv_win.getch()
        inv_win.clear()
        screen.refresh()
        inv_win.refresh()
        
    def get_turn_order(choice_1, choice_2):
        priority_1 = battle.turn_priority(choice_1)
        priority_2 = battle.turn_priority(choice_2)
        if priority_1 > priority_2:
            return 1
        elif priority_2 < priority_1:
            return 2
        else:
            return battle.compare_speed(player_1.poke, player_2.poke)
        return
    
    def execute_choice(choice, player):
        if choice[0] == 'switch':
            player.poke = player.team.get_Member(choice[1])
        return
    
    def game_over():
        return False
    
    def end_game():
        return
    
    box1 = curses.newwin(7, 17, 17, 61)
    box2 = curses.newwin(7, 57, 17, 2)
    p1_box = curses.newwin(5, 26, 12, 52)
    p2_box = curses.newwin(5, 26, 1, 2)
    box1_dims = box1.getmaxyx()
    box2_dims = box2.getmaxyx()
    player_1.poke = player_1.team.get_Member(pick_poke(player_1, False))
    player_2.poke = player_2.team.get_Member(pick_poke(player_2, False))
    
    quit = False
    while quit == False:
        turn_setup()
        p1_choice, p2_choice, quit = get_choices()
        if quit:
            break
        first_player = get_turn_order(p1_choice, p2_choice)
        if first_player == 1:
            p1 = player_1
            p2 = player_2
            first_choice = p1_choice
            second_choice = p2_choice
        else:
            p1 = player_2
            p2 = player_1
            first_choice = p2_choice
            second_choice = p1_choice
        execute_choice(first_choice, p1)
        if game_over():
            end_game()
        execute_choice(second_choice, p2)
        if game_over():
            end_game()
        turn_breakdown()
        
    battle_menu()
        
def select_team(player):
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    teams = save.get_Files('TEAM')
    lines = ['Team', 'Member_1', 'Member_2', 'Member_3', 'Member_4', 'Member_5', 'Member_6', 'Confirm']
    title = player + ' Team Selection'
    #Create dictionaries needed to support selections
    vals = dict(zip(range(len(lines)), [0]*len(lines)))
    strvals = dict(zip(range(len(lines)), ['']*len(lines)))
    maxval = dict(zip(range(len(lines)), [1]*len(lines)))
    #Set max unique values for each option
    maxval[0] = len(teams)
    while selection < 0:
        # Display Static Information
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        screen.clear()
        screen.addstr(1, (dims[1]-len(title))/2, title, curses.A_BOLD)
        for i, l in enumerate(lines):
            screen.addstr(2*i+3, 1, l, graphics[i])
        screen.border()
        # Update string values for each option
        strvals[0] = teams[vals[0]]
        # Grab team
        team = save.load_Team(strvals[0])
        # Update string values with poke
        for i in range(1, 7):
            if team.pos_open(i):
                strvals[i] = ''
            else:
                poke = team.get_Member(i)
                strvals[i] = poke.Name
        # Display Current Choices
        for i in range(len(lines)-1):
            screen.addstr(2*i+3, len(lines[i])+2, strvals[i])
        # Flush to Screne
        screen.refresh()
        # Key Stuff
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == curses.KEY_LEFT:
            vals[option] = (vals[option]-1)%maxval[option]
        elif action == curses.KEY_RIGHT:
            vals[option] = (vals[option]+1)%maxval[option]
        elif action == ord('\n'):
            if option == 0:
                d_team(team)
            elif option in range(1, 7):
                d_poke(team.get_Member(option))
            elif option == 7:
                selection = option
        elif action == ord('q'):
            selection = option
        elif action == ord('d'):
            d_team(team)
        screen.refresh()
    screen.clear()
    return team

def select_poke(team, max_pkmn):
    """Choose which poke from the team will be used in battle"""
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    lines = [team.get_Member(i).Name for i in range(1, 7)] + ['Confirm']
    title = 'Team Selection'
    n_chosen = 0
    #Create dictionaries needed to support selections
    vals = dict(zip(range(len(lines)), [0]*(len(lines)-1)))
    strvals = dict(zip(range(len(lines)), ['[ ]']*(len(lines)-1)))
    maxval = dict(zip(range(len(lines)), [1]*(len(lines)-1)))
    #Set max unique values for each option
    maxval[0] = len(lines)
    while selection < 0:
        # Display Static Information
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        screen.clear()
        screen.addstr(1, (dims[1]-len(title))/2, title)
        for i, l in enumerate(lines):
            screen.addstr(2*i+3, 5, l, graphics[i])
        screen.border()
        # Display Current Choices
        for i in range(len(lines)-1):
            screen.addstr(2*i+3, 1, strvals[i])
        # Flush to Screen
        screen.refresh()
        # Key Stuff
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == ord('\n'):
            if option in range(6):
                d_poke(team.get_Member(option+1))
            elif option == 6:
                selection = option
        elif action == ord(' '):
            if option in range(6):
                if strvals[option] == '[ ]' and n_chosen < max_pkmn:
                    vals[option] = 1
                    strvals[option] = '[X]'
                    n_chosen += 1
                elif strvals[option] == '[X]':
                    vals[option] = 0
                    strvals[option] = '[ ]'
                    n_chosen -= 1
        elif action == ord('q'):
            selection = option
        elif action == ord('d'):
            d_team(team)
        screen.refresh()
    screen.clear()
    return vals
    
def under_Construction():
    temp = dict()
    temp['opt_a'] = [1, 2, 3]
    temp['opt_b'] = [1, 2]
    temp['opt_c'] = [1]
    temp['opt_d'] = ['alpha', 'beta', 'gamma', 'radiation']
    x = user_options(temp)
    screen.nodelay(0)
    screen.clear()
    screen.addstr(dims[0]/2, dims[1]/2-9, 'Under Construction')
    screen.refresh()
    screen.getch()
    
def standard_menu(lines):
    """
    Displays a screen with the choices passed into 'lines'. Returns the choice selected by the user.
    """
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    while selection < 0:
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        title = 'TogePy'
        screen.addstr(0, (dims[1] - len(title))/2, title) #Show Title
        for i, l in enumerate(lines):
            screen.addstr((dims[0] - len(lines))/2 + i, (dims[1] - len(l))/2, l, graphics[i])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == ord('\n'):
            selection = option
        elif action == ord('q'):
            selection = len(lines)-1
        screen.refresh()
    screen.clear()
    return selection
    
def popup_menu(lines):
    """
    Pops up a new window centered on the main screen with the choices passed into 'lines'. Returns the choice selected by the user.
    """
    n_rows = len(lines)+2
    n_cols = max([len(l) for l in lines])+2
    begin_y = (dims[0] - n_rows)/2
    begin_x = (dims[1] - n_cols)/2
    sub = screen.subwin(n_rows, n_cols, begin_y, begin_x)
    sub.nodelay(0)
    sub.clear()
    selection = -1
    option = 0
    while selection < 0:
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        sub.border()
        for i, l in enumerate(lines):
            sub.addstr(i+1, (n_cols - len(l))/2, l, graphics[i])
        sub.refresh()
        action = sub.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == ord('\n'):
            selection = option
        elif action == ord('q'):
            selection = n_rows-3
        sub.refresh()
    sub.clear()
    sub.refresh()
    screen.redrawwin()
    screen.refresh()
    return selection

def user_options(d_settings, title='Select Options'):
    """
    Displays a screen where users can set values for multiple game settings. d_settings should be a dictionary where the keys correspond to the game values that are being set and the dictionary values are lists of the allowable options for each setting.
    """
    d_uservals = dict()
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    lines = d_settings.keys() + ['Confirm']
    #Create dictionaries needed to support selections
    vals = dict(zip(range(len(lines)), [0]*len(lines)))
    strvals = dict(zip(range(len(lines)), ['']*len(lines)))
    maxval = dict(zip(range(len(lines)), [1]*len(lines)))
    #Set max unique values for each option
    maxval = [len(l) for l in d_settings.values()]
    while selection < 0:
        # Display Static Information
        graphics = [0]*len(lines)
        graphics[option] = curses.A_REVERSE
        screen.clear()
        screen.addstr(1, (dims[1]-len(title))/2, title)
        for i, l in enumerate(lines):
            screen.addstr(i+3, 1, l, graphics[i])
        screen.border()
        # Update string values for each option
        strvals = [str(d_settings[k][vals[i]]) for i, k in enumerate(lines[:-1])]
        # Display Current Choices
        for i in range(len(lines)-1):
            screen.addstr(i+3, len(lines[i])+2, strvals[i])
        # Flush to Screne        
        screen.refresh()
        # Key Stuff
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%len(lines)
        elif action == curses.KEY_DOWN:
            option = (option + 1)%len(lines)
        elif action == curses.KEY_LEFT:
            vals[option] = (vals[option]-1)%maxval[option]
        elif action == curses.KEY_RIGHT:
            vals[option] = (vals[option]+1)%maxval[option]
        elif action == ord('\n') and option == (len(lines)-1):
            selection = option
        elif action == ord('q'):
            selection = option
        elif action == ord('d'):
            d_team(team)
        screen.refresh()
    screen.clear()
    d_uservals = dict(zip(lines[:-1], strvals))
    return d_uservals


def scrolling_list(choices, screen, ymin, ymax, xmin, xmax):
    return 'beh'

if __name__ == '__main__':
    try:
        intro()
        menu()
        screen.clear()
        screen.refresh()
        curses.endwin()
    except Exception:
        screen.clear()
        screen.refresh()
        curses.endwin()
        raise