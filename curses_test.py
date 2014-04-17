import curses

screen = curses.initscr()
screen.clear()
screen.border()
screen.refresh()
sub = screen.subwin(10,10)
sub.border()
sub.addstr(1,1,'test')
sub.refresh()
b = sub.getch()
sub.clear()
sub.refresh()
a = screen.getch()