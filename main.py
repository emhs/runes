#!/usr/bin/env python
import os
import sys
import urwid
import argparse
import random
import yaml
from runes import architecture
from runes import creature
from runes import architecture

# Detect OS and select appropriate data directory
if sys.platform.startswith('linux') or sys.platform == 'cygwin':
    data_dir = os.path.join(os.environ['HOME'], '.runes')
elif sys.platform.startswith('win'):
    data_dir = os.path.join(os.environ['APPDATA'], 'runes')
elif sys.platform == 'darwin':
    data_dir = os.path.join(os.environ['HOME'], 'Library', 'runes')

# Create data directory if it does not exist
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# Read config file if it exists
config_path = os.path.join(data_dir, 'runes.conf')
if os.path.exists(config_path):
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)
else:
    config = {
              'numpad' : False
              }
    # Default config goes here.

save_path = os.path.join(data_dir, 'runes.save')
if os.path.exists(save_path):
    with open(save_path) as save_file:
        loaded_game = yaml.safe_load(save_file)
        random.setstate(loaded_game[state])
        # TODO: More game state here.

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
do_function = {}
command_function = {}

# Standard actions in the form of do_*

def do_go(key):
    global command
    command = ''
    output = []
    output.extend(player.go(direction_keys[key]))
    return output
do_function['go'] = do_go

def do_open(key):
    global command
    command = 'open'
    output = []
    return output
do_function['open'] = do_open

def do_close(key):
    global command
    command = 'close'
    output = []
    return output
do_function['close'] = do_close

def do_quit(key):
    raise urwid.ExitMainLoop()
do_function['quit'] = do_quit

# Extended command functions in the form of command_*

def command_open(key):
    global command
    output = []
    if key in direction_keys:
        output.extend(player.open_door(direction_keys[key]))
    command = ''
    return output
command_function['open'] = command_open

def command_close(key):
    global command
    output = []
    if key in direction_keys:
        output.extend(player.close_door(direction_keys[key]))
    command = ''
    return output
command_function['close'] = command_close

# Set keyboard mapping
keymap = {}
keymap['o'] = 'open'
keymap['c'] = 'close'
keymap['Q'] = 'quit'
keymap['S'] = 'save'

# Set direction keys based on numpad config option
if config['numpad']:
    direction_keys = {
            '1': 'southwest',
            '2': 'south', 
            '3': 'southeast',
            '6': 'east', 
            '9': 'northeast', 
            '8': 'north', 
            '7': 'northwest',
            '4': 'west'}
else:
    direction_keys = {
            'h': 'west',
            'j': 'south',
            'k': 'north',
            'l': 'east',
            'u': 'northeast',
            'y': 'northwest',
            'b': 'southwest',
            'n': 'southeast'}

# Add direction keys to keymap
for key in direction_keys.keys():
    keymap[key] = 'go'

def handle_keys(key):
    global command
    output = []
    if command:
        output.extend(command_function[command](key))
    else:
        output.extend(do_function[keymap[key]](key))
    if output:
        output = output_filter(output, args)
        messages.body.contents.extend(map(urwid.Text, output))
        messages.body.set_focus(messages.body.get_focus()[1] + len(output))

    # Re-render map after turn
    map_box.set_text(('map', active_map.render()))

if __name__ == '__main__':
    # Initialize map and player
    active_map = level.Map(architecture.Cell())
    player = creature.Player(pos=active_map.cell(8, 8))
    active_map.draw_shape(((10, 10), (10, 20), (20, 20), (20, 10)), closed=True)
    active_map.draw_point((15, 20), type='door')

    # Initialize layout
    map_box = urwid.Text(('map', active_map.render()))
    status_bar = urwid.Text(('status', 'Running...'))
    div = urwid.Divider()
    messages = urwid.ListBox([urwid.Text('Welcome to RUNES')])
    pile = urwid.Pile([('pack', map_box), ('pack', status_bar), ('pack',
        div), messages])

    palette = [
            ('map', 'default', 'default'),
            ('player', 'bold', 'default'),
            ('debug', 'light gray', 'default'),
            ('info', 'dark gray', 'default'),
            ('warn', 'dark red', 'default'), ]

    loop = urwid.MainLoop(pile, palette, unhandled_input=handle_keys)
    loop.run()
