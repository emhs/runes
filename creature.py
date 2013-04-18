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

