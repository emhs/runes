#!/usr/bin/env python
import urwid
import argparse
from runes import architecture
from runes import creature
from runes import architecture

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

def handle_keys(key):
    global command
    output = []
    if command:
        output.extend(command_function[command](key))
    else:
        # Movement keys
        if key in direction_keys:
            output.extend(player.go(direction_keys[key]))
        # Doors
        elif key == 'o':
            command = 'open'
        elif key == 'c':
            command = 'close'
        # Exit game
        elif key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
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
