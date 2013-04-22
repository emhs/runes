dir = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest',
        'west', 'northwest']

class Error(Exception):
    """Base class for creature exceptions"""
    pass

class MovementBlocked(Error):
    """Exception raised for movement to a blocked destination cell.
    
    Attributes:
        dest -- blocked destination cell
    """
    
    def __init__(self, dest):
        self.dest = dest

class CellOccupied(Error):
    """Exception raised if the destination cell is occupied.
    
    Attributes:
        dest     -- blocked destination cell
        creature -- creature blocking movement
    """
    
    def __init__(self, dest, creature=None):
        self.dest = dest
        if creature:
            self.creature = creature
        else:
            self.creature = dest.creature

class InvalidDirection(Error):
    """Exception raised on attempt to move in an invalid direction.
    
    Attributes:
        direction   -- attempted movement direction
    """
    
    def __init__(self, dir):
        self.direction = dir

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
    
    def go(self, dirr):
        output = []
        dest = self.position.adjacent[dirr]
        if dest:
            output.extend(self._bamf(dest))
            output.extend([('debug', 'Moved {dir}'.format(dir=dirr))])
        else:
            output.extend([('info', 'I think that\'s a wall ',format(dir=dirr))])
    
    def render(self):
        return self.character

    def open_door(self, dirr):
        output = []
        if self.door:
            self.position.adjacent[dirr].open_door()
            output.extend([('debug', 'Opened door to the '
                '{dirr}'.format(dirr=dirr))])
        else:
            output.extend([('info', 'There\'s no door there')])
        return output
    
class Player(Creature):
    def __init__(self, pos, inv=[]):
        Creature.__init__(self, pos, inv)
        self.character = ('player', '@')
