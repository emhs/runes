#!/usr/bin/env python
import sys
import urwid
from runes import architecture
from runes import map
from runes import creature

def handle_keys(key):
    # Movement keys
    if key == 'h':
        player.go_west()
    elif key == 'j':
        player.go_south()
    elif key == 'k':
        player.go_north()
    elif key == 'l':
        player.go_east()
    elif key == 'u':
        player.go_northeast()
    elif key == 'y':
        player.go_northwest()
    elif key == 'n':
        player.go_southeast()
    elif key == 'b':
        player.go_southwest()
    # Exit game
    elif key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    
    # Re-render map after turn
    map_box.set_text(('map', active_map.render()))

def main():
    # Initialize map and player
    active_map = map.Map(architecture.Cell())
    player = creature.Player(pos=active_map.map[8][8])
    
    # Initialize layout
    map_box = urwid.Text(('map', active_map.render()))
    status_bar = urwid.Text(('status', 'Running...'))
    div = urwid.Divider()
    messages = urwid.ListBox([urwid.Text('Welcome to RUNES')])
    pile = urwid.Pile([map_box, status_bar, div, urwid.BoxAdapter(messages, 2)])
    top = urwid.Filler(pile, valign='top')
    
    loop = urwid.MainLoop(top, unhandled_input=handle_keys)
    loop.run()

if __name__ == '__main__':
    main()