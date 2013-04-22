#!/usr/bin/env python
import sys
import urwid
import argparse
from runes import architecture
from runes import level
from runes import creature

parser = argparse.ArgumentParser(prog='RUNES', description='Reality '
        'Undermining Magical Exploration Simulation\n\n'
        'RUNES is a roguelike with a complex and flexible magic system.')
parser.add_argument('-d', '--debug', action='store_true', 
        dest='debug', help='Print debugging messages')
parser.add_argument('-v', '--verbose', action='store_true',
        dest='verbose', help='Print informational messages')

args = parser.parse_args()

def output_filter(output, args):
    if not args.debug:
        output = [line for line in output if line[0] != 'debug']
    if not args.verbose:
        output = [line for line in output if line[0] != 'info']
    return output

command = ''
command_function = {}
direction_keys = {
        'h': 'west',
        'j': 'south',
        'k': 'north',
        'l': 'east',
        'u': 'northeast',
        'y': 'northwest',
        'b': 'southwest',
        'n': 'southeast'}

def command_open(key):
    if key in direction_keys:
        output = []
        output.extend(player.open_door(direction_keys[key]))
        command = ''
        return output
command_function['open'] = command_open

def handle_keys(key):
    global command
    output = []
    if command:
        output.extend(command_function[command](key))
    # Movement keys
    if key in direction_keys:
        output.extend(player.go(direction_keys[key]))
    # Doors
    elif key == 'o':
        command = 'open'
    # Exit game
    elif key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    if output:
        output = output_filter(output, args)
        messages.body.contents.extend(map(urwid.Text, output))
        messages.body.set_focus(messages.body.get_focus()[1]+len(output))
    
    # Re-render map after turn
    map_box.set_text(('map', active_map.render()))

if __name__ == '__main__':
    # Initialize map and player
    active_map = level.Map(architecture.Cell())
    player = creature.Player(pos=active_map.map[8][8])
    active_map.draw_shape(((10,10), (10,20), (20,20), (20, 10)), closed=True)
    
    # Initialize layout
    map_box = urwid.Text(('map', active_map.render()))
    status_bar = urwid.Text(('status', 'Running...'))
    div = urwid.Divider()
    messages = urwid.ListBox([urwid.Text('Welcome to RUNES')])
    pile = urwid.Pile([('pack', map_box), ('pack', status_bar), ('pack',
        div), messages])
    
    loop = urwid.MainLoop(pile, unhandled_input=handle_keys)
    loop.run()
