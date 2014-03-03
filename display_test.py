import curses
import pkmn_test
import numpy as np

screen = curses.initscr()
screen.clear()
screen.refresh()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
curses.start_color()
dims = screen.getmaxyx()

def scrolling_list(choices, screen, ymin, ymax, xmin, xmax):
    return 'beh'

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
    screen.getch()
    screen.clear()
    
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
    elif 1 <= selection <= 3:
        under_Construction()
        menu()
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
            Item = int(pk.Item)
            sts = str(pk.Status)
            if sts == 'None':
                sts = '---'
            screen.addstr(3*i+2, 64, 'Item: ['+('X'*Item).ljust(1,' ')+']')
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
    
def under_Construction():
    screen.nodelay(0)
    screen.clear()
    screen.addstr(dims[0]/2, dims[1]/2-9, 'Under Construction')
    screen.refresh()
    screen.getch()

if __name__ == '__main__':
    intro()
    menu()
    curses.endwin()