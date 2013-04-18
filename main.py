#!/usr/bin/env python
import curses
import curses.wrapper
from runes import architecture
from runes import map
from runes import creature

def main(stdscr):
    curses.cbreak()
    curses.curs_set(0)
    # Initialize map_window to display the map
    map_height = 21
    map_width = 80
    map_start_x = 0
    map_start_y = 0
    map_window = curses.newwin(map_height, map_width, map_start_y, map_start_x)
    map_window.border()
    
    # Initialize map and player
    active_map = map.Map(architecture.Cell())
    player = creature.Player(pos=active_map.map[8][8])
    
    # Initial render
    map_render = active_map.render()
    for row in range(21):
        for col in range(80):
            map_window.addstr(row, col, *map_render[row][col])
    
    # Main loop
    char = stdscr.getkey()
    while char != 'Q':
        if char == 'h':
            player.go_west()
        elif char == 'j':
            player.go_south()
        elif char == 'k':
            player.go_north()
        elif char == 'l':
            player.go_east()
        elif char == 'u':
            player.go_northeast()
        elif char == 'y':
            player.go_northwest()
        elif char == 'n':
            player.go_southeast()
        elif char == 'b':
            player.go_southwest()
        # Re-render map
        map_render = active_map.render()
        for row in range(21):
            for col in range(80):
                map_window.addstr(row, col, *map_render[row][col])
        char = stdscr.getkey()
    
    curses.nocbreak()

if __name__ == '__main__':
    curses.wrapper(main)