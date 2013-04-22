class Cell():
    """Base map cell.
    
    Attributes:
        creature        -- creature (if any) in the cell
        contents        -- list of items within the cell
        inscriptions    -- runic inscriptions on this cell
        adjacent        -- list of adjacent cells (clockwise starting at north)
    
    Flags:
        open            -- cell passable
        lit             -- cell lit by a light source
        glow            -- cell permanently lit by its own light source
        seen            -- ceel is in player FOV
    """
    
    def __init__(self, contents=[], inscriptions=[], creature=None, open=True, 
            door=False, lit=False, seen=False, glow=False):
        self.open = open # Cell passabiliy
        self.door = door
        self.lit = lit # Cell is in range and LOS of a light source
        self.seen = seen # Cell is in player FOV
        self.glow = glow # Cell is permanently lit by its own light source
        self.creature = creature # Creature (if any) occupying the cell
        self.contents = contents # Objects contained within the cell
        self.inscriptions = inscriptions # Runic inscriptions on this cell
        self.adjacent = []

    def character(self):
        if not self.open:
            if self.door:
                char = '+'
            else:
                char = '#'
        else:
            if self.door:
                char = '-'
            else:
                char = '.'
        return char
    
    def render(self):
        if self.creature:
            return self.creature.render()
        elif self.contents:
            return self.contents[0].render()
        elif self.inscriptions:
            return self.inscriptions[0].render()
        else:
            return self.character()

    def open_door(self):
        if self.door:
            self.open = True
    
def wall(contents=[], inscriptions=[], creature=[], open=False, door=False, 
        lit=False, seen=False, glow=False):
    return Cell(contents, inscriptions, creature, open, lit, seen, glow)
