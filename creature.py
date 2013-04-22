dir = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest',
        'west', 'northwest']

class Creature():
    """Base creature class
    
    Attributes:
        position    -- current location
        inventory   -- items held by the creature
    
    Methods:
        go(dir)     -- Go to the next adjacent cell to the <dir> (Can be north, 
                        south, east, west, northeast, southeast, southwest, or 
                        northwest)
        _bamf(dest) -- Teleport the creature to destination Cell dest
    """
    
    def __init__(self, pos, inv=[]):
        self.position = pos
        self.position.creature = self
        self.inventory = inv
        self.character = ('creature', 'm')
    
    def _bamf(self, dest):
        output = []
        if not dest.open:
            output.extend([('debug', 'Can\'t go there')])
        elif dest.creature:
            output.extend([('debug', 'Occupied')])
        else:
            self.position.creature = None
            dest.creature = self
            self.position = dest
            output.extend([('debug', 'Bamf!')])
        return output
    
    def go(self, dirr):
        output = []
        dest = self.position.adjacent[dirr]
        if dest:
            output.extend([('debug', 'Tried to move {dir}'.format(dir=dirr))])
            output.extend(self._bamf(dest))
        else:
            output.extend([('info', 'I think that\'s a wall')])
        return output
    
    def render(self):
        return self.character

    def open_door(self, dirr):
        output = []
        dest = self.position.adjacent[dirr]
        if dest.door:
            dest.open_door()
            output.extend([('debug', 'Opened door to the '
                '{dirr}'.format(dirr=dirr))])
        else:
            output.extend([('info', 'There\'s no door there')])
        return output
    
class Player(Creature):
    def __init__(self, pos, inv=[]):
        Creature.__init__(self, pos, inv)
        self.character = ('player', '@')
