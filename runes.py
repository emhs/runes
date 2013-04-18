#!/usr/bin/env python
import curses
import curses.wrapper
from runes import architecture
from runes import map
from runes import creature

def main(stdscr):
    curses.curs_set(0)
    # Initialize map_window to display the map
    map_height = 21
    map_width = 80
    map_start_x = 0
    map_start_y = 0
    map_window = curses.newwin(map_height, map_width, map_start_y, map_start_x)
    map_window.border()
    
    

if __name__ == '__main__':
    curses.wrapper.wrapper(main)