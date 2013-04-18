import curses

class Cell():
    def __init__(self, contents=[], inscriptions=[], creature=None, open=True, 
            lit=False, seen=False, glow=False):
        self.open = open # Cell passabiliy
        self.lit = lit # Cell is in range and LOS of a light source
        self.seen = seen # Cell is in player FOV
        self.glow = glow # Cell is permanently lit by its own light source
        self.creature = creature # Creature (if any) occupying the cell
        self.contents = contents # Objects contained within the cell
        self.inscriptions = inscriptions # Runic inscriptions on this cell
    
def wall(contents=[], inscriptions=[], creature=[], open=False, lit=False, 
        seen=False, glow=False):
    return Cell(contents, inscriptions, creature, open, lit, seen, glow)