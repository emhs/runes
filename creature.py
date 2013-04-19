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
        go_<dir>()  -- Go to the next adjacent cell to the <dir> (Can be north, 
                        south, east, west, northeast, southeast, southwest, or 
                        northwest)
        go(dir)     -- Alias to the appropriate go_<dir>() method
        _bamf(dest) -- Teleport the creature to destination Cell dest
    """
    
    def __init__(self, pos, inv=[]):
        self.position = pos
        self.position.creature = self
        self.inventory = inv
        self.character = 'm'
    
    def _bamf(self, dest):
        if not dest.open:
            raise MovementBlocked(dest)
        elif dest.creature:
            raise CellOccupied(dest)
        else:
            self.position.creature = None
            dest.creature = self
            self.position = dest
    
    def go(self, dir):
        try:
            move = getattr(self, "go_" + dir)
            move()
        except:
            raise InvalidDirection(dir)
    
    def go_north(self):
        dest = self.position.adjacent[0]
        if not dest:
            raise InvalidDirection('north')
        _bamf(dest)
    
    def go_northeast(self):
        dest = self.position.adjacent[1]
        if not dest:
            raise InvalidDirection('northeast')
        _bamf(dest)
    
    def go_east(self):
        dest = self.position.adjacent[2]
        if not dest:
            raise InvalidDirection('east')
        _bamf(dest)
    
    def go_southeast(self):
        dest = self.position.adjacent[3]
        if not dest:
            raise InvalidDirection('southeast')
        _bamf(dest)
    
    def go_south(self):
        dest = self.position.adjacent[4]
        if not dest:
            raise InvalidDirection('south')
        _bamf(dest)
    
    def go_southwest(self):
        dest = self.position.adjacent[5]
        if not dest:
            raise InvalidDirection('southwest')
        _bamf(dest)
    
    def go_west(self):
        dest = self.position.adjacent[6]
        if not dest:
            raise InvalidDirection('west')
        _bamf(dest)
    
    def go_northwest(self):
        dest = self.position.adjacent[7]
        if not dest:
            raise InvalidDirection('northwest')
        _bamf(dest)
    
    def render(self):
        return self.character
    
class Player(Creature):
    def __init__(self, pos, inv=[]):
        Creature.__init__(self, pos, inv)
        self.character = ('player', '@')