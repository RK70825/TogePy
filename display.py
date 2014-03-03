"""
togePy.display

This module handles the display in togePy
"""
import curses
import time
import random

startlength = 5
growlength = 2
speeds = {'Easy':0.1, 'Medium':0.06, 'Hard':0.04}
difficulty = 'Medium'
acceleration = False
highscore = 0
screen = curses.initscr()
curses.noecho()
dims = screen.getmaxyx()
screen.keypad(1)
screen.clear()

def game():
    screen.clear()
    screen.nodelay(1)
    head = [1, 1]
    body = [head[:]]*startlength
    screen.border()
    direction = 0 # 0: right, 1: down, 2: left, 3: up
    gameover = False
    foodmade = False
    deadcell = body[-1][:]
    while not gameover:
        global highscore
        while not foodmade:
            y, x = random.randrange(1, dims[0]-1), random.randrange(1, dims[1]-1)
            if screen.inch(y, x) == ord(' '):
                foodmade = True
                screen.addch(y, x, ord('@'))
        if deadcell not in body:
            screen.addch(deadcell[0], deadcell[1], ' ')
        screen.addch(head[0], head[1], 'X')
        
        action = screen.getch()
        if action == curses.KEY_UP and direction !=1:
            direction = 3
        elif action == curses.KEY_DOWN and direction !=3:
            direction = 1
        elif action == curses.KEY_RIGHT and direction !=2:
            direction = 0
        elif action == curses.KEY_LEFT and direction != 0:
            direction = 2
        if direction == 0:
            head[1] += 1
        elif direction == 2:
            head[1] -= 1
        elif direction == 1:
            head[0] += 1
        elif direction == 3:
            head[0] -= 1
        
        deadcell = body[-1][:]
        for z in range(len(body) - 1, 0, -1):
            body[z] = body[z-1][:]
        
        body[0] = head[:]
        
        if screen.inch(head[0], head[1]) != ord(' '):
            if screen.inch(head[0], head[1]) == ord('@'):
                foodmade = False
                for z in range(growlength):
                    body.append(body[-1])
            else:
                gameover = True
        curses.curs_set(0)
        screen.refresh()
        if not acceleration:
            time.sleep(speeds[difficulty])
        else:
            time.sleep(15.*speeds[difficulty]/len(body))
    screen.clear()
    screen.nodelay(0)
    score = (len(body)-startlength)/growlength
    message1 = 'Game Over'
    message2 = 'You got '+str(score)+' points'
    message3 = 'Press Enter to play again'
    message4 = 'Press Space to quit'
    message5 = 'Press M to go to the menu'
    screen.addstr(dims[0]/2-2, (dims[1] - len(message1))/2 - 1, message1)
    screen.addstr(dims[0]/2-1, (dims[1] - len(message2))/2 - 1, message2)
    screen.addstr(dims[0]/2, (dims[1] - len(message3))/2 - 1, message3)
    screen.addstr(dims[0]/2+1, (dims[1] - len(message4))/2 - 1, message4)
    screen.addstr(dims[0]/2+2, (dims[1] - len(message5))/2 - 1, message5)    
    screen.refresh()
    if score > highscore:
        highscore = score
    q = 0
    while q not in [32, 10, 77, 109]:
        q = screen.getch()
    if q == 10:
        screen.clear()
        game()
    if q == 77 or q == 109:
        menu()

def menu():
    screen.nodelay(0)
    screen.clear()
    selection = -1
    option = 0
    while selection < 0:
        graphics = [0]*5
        graphics[option] = curses.A_REVERSE
        screen.addstr(0, dims[1]/2 - 3,'Snake')
        screen.addstr(dims[0]/2-2, dims[1]/2-2, 'Play', graphics[0])
        screen.addstr(dims[0]/2-1, dims[1]/2-6, 'Instructions', graphics[1])
        screen.addstr(dims[0]/2, dims[1]/2-6, 'Game Options', graphics[2])
        screen.addstr(dims[0]/2+1, dims[1]/2-5, 'High Scores', graphics[3])
        screen.addstr(dims[0]/2+2, dims[1]/2-2, 'Exit', graphics[4])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%5
        elif action == curses.KEY_DOWN:
            option = (option + 1)%5
        elif action == ord('\n'):
            selection = option
    screen.clear()
    if selection == 0:
        game()
    elif selection == 1:
        instructions()
    elif selection == 2:
        gameoptions()

def instructions():
    screen.clear()
    screen.nodelay(0)
    lines = ['Use the arrow keys to move', 'Don\'t run into the wall or yourself', 'Eat food to grow','','Press any key to go back']
    for z, l in enumerate(lines):
        screen.addstr((dims[0] - len(lines))/2 + z, (dims[1] - len(l))/2, l)
    screen.refresh()
    screen.getch()
    menu()
    
def gameoptions():
    global startlength, growlength, difficulty, acceleration
    screen.clear()
    screen.nodelay(0)
    selection = -1
    option = 0
    while selection <4:
        screen.clear()
        graphics = [0]*5
        graphics[option] = curses.A_REVERSE        
        strings = ['Starting Snake Length: '+str(startlength), 'Snake Growth rate: '+str(growlength), 'Difficulty: '+difficulty, 'Acceleration: '+str(acceleration), 'Exit']
        for z in range(len(strings)):
            screen.addstr((dims[0]-len(strings))/2+z, (dims[1]-len(strings[z]))/2, strings[z], graphics[z])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1)%5
        elif action == curses.KEY_DOWN:
            option = (option + 1)%5
        elif action == ord('\n'):
            selection = option
        elif action == curses.KEY_RIGHT:
            if option == 0 and startlength < 20:
                startlength += 1
            elif option ==1 and growlength < 10:
                growlength += 1
        elif action == curses.KEY_LEFT:
            if option == 0 and startlength > 1:
                startlength -= 1
            elif option == 1 and growlength > 1:
                growlength -= 1
        if selection == 3:
            acceleration = not acceleration
        elif selection == 2:
            if difficulty == 'Easy':
                difficulty = 'Medium'
            elif difficulty == 'Medium':
                difficulty = 'Hard'
            else:
                difficulty = 'Easy'
        if selection < 4:
            selection = -1
    menu()    
            
menu()
curses.endwin()









#import curses
#import time
#screen = curses.initscr()
#curses.noecho()
#screen.keypad(1)
#screen.border()
#dims = screen.getmaxyx() #returns (24, 80)
#curses.curs_set(0)
#q = -1
#x, y = 1, 1
#Vertical = 1
#Horizontal = 1
#while q != ord('q'):
    #screen.addch(y, x, ord('@'))
    #screen.move(dims[0]-1, dims[1]-1)
    #screen.refresh()
    #q = screen.getch()
    #if q == curses.KEY_UP and y > 1:
        #screen.addch(y, x, ' ')
        #y -= 1
    #elif q == curses.KEY_DOWN and y < dims[0] - 2:
        #screen.addch(y, x, ' ')
        #y += 1
    #elif q == curses.KEY_LEFT and x > 1:
        #screen.addch(y, x, ' ')
        #x -= 1
    #elif q == curses.KEY_RIGHT and x < dims[1] - 2:
        #screen.addch(y, x, ' ')
        #x += 1
#screen.getch()
#curses.endwin()



#message = raw_input('Enter message desired: ')
#q, vertical, horizontal = -1, 1, 1
#y, x = 0, 0
#screen = curses.initscr()
#curses.start_color()
#curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
#curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
#curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
#g = 0
#bold = 0
#reverse = 0
#b = [curses.A_NORMAL, curses.A_BOLD]
#r = [curses.A_NORMAL, curses.A_REVERSE]
#screen.nodelay(1)
#curses.noecho()
#dims = screen.getmaxyx()
#while q <0 or q in range(48, 52) or q in [98, 114]:
    #q = screen.getch()
    #if q in range(48,52):
        #g = int(chr(q))
    #elif q == 98:
        #bold = (bold + 1) % 2
    #elif q == 114:
        #reverse = (reverse + 1) % 2
    #screen.clear()
    #screen.addstr(y, x, message, curses.color_pair(g) | b[bold] | r[reverse])
    #y += vertical
    #x += horizontal
    #if y == dims[0]-1:
        #vertical = -1
    #elif y == 0:
        #vertical = 1
    #if x == dims[1] - len(message) - 1:
        #horizontal = -1
    #elif x == 0:
        #horizontal = 1
    #time.sleep(0.05)
#curses.endwin()