import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr('Welcome to the typing speed test!')
    stdscr.addstr('\nPress any key to begin')
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f'WPM: {wpm}')
    
    for i, char in enumerate(current):
        if char == target[i]:
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(2)
        
        stdscr.addstr(0, i, char, color)

def wpm_test(stdscr):
    target_text = "Hello World! This is some test text for this app."
    try:
        with open('text.txt', 'r') as f:
            lines = f.readlines()
            target_text = random.choice(lines)
    except:
        pass
    
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        elapsed_time = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (elapsed_time/60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if ''.join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def end_screen(stdscr):
    stdscr.addstr(2, 0, 'You completed the test! Press any key to play again')
    key = stdscr.getkey()
    if ord(key) == 27:
        return False
    else:
        return True

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    run = True
    start_screen(stdscr)
    while run:
        wpm_test(stdscr)
        run = end_screen(stdscr)

wrapper(main)