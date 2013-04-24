from runes import architecture
from copy import deepcopy

def adjacent_cells(row, col, grid):
    """Generates a list of adjacent cells, given a position and grid of cells.
    
    Arguments:
        row, col    -- position of the current cell in the grid
        grid        -- grid of cells
    """
    
    adjacents = {}
    
    coordinates = ((row-1, col, 'north'), (row-1, col+1, 'northeast'),
            (row, col+1, 'east'), (row+1, col+1, 'southeast'), 
            (row+1, col, 'south'), (row+1, col-1, 'southwest'), 
            (row, col-1, 'west'), (row-1, col-1, 'northwest'))
    for rr, cc, dir in coordinates:
        if rr<0 or cc<0:
            adjacents[dir] = None
        elif rr>=21:
            adjacents[dir] = None
        elif cc>=80:
            adjacents[dir] = None
        else:
            adjacents[dir] = grid[rr][cc]
    
    return adjacents

class Map():
    def __init__(self, default, cells=()):
        # Initialize map with default cell
        self.map = [[deepcopy(default) for _ in range(80)] for _ in range(21)]
        
        # Load pre-specified cells
        for row, col, cell in cells:
            self.map[row][col] = cell
        
        # Build adjacents
        for row in range(21):
            for col in range(80):
                self.map[row][col].adjacent = adjacent_cells(row, col, self.map)
    
    def render(self):
        rendered = [[cell.render() for cell in row] for row in self.map]
        result = []
        for row in rendered:
            row.append('\n')
            result.extend(row)
        return result

    def draw_point(self, point, type='wall'):
        if type == 'wall':
            self.map[point[0]][point[1]].open = False
        elif type == 'floor':
            self.map[point[0]][point[1]].open = True
            self.map[point[0]][point[1]].open = False
        elif type == 'door':
            self.map[point[0]][point[1]].open = False
            self.map[point[0]][point[1]].door = True

    def draw_line(self, start, end, type='wall'):
        y0, x0 = start
        y1, x1 = end
        dy = y1-y0
        dx = x1-x0
        dy_sign = 1 if dy >= 0 else -1
        dx_sign = 1 if dx >= 0 else -1
        if dy == 0:
            for x in range(x0, x1, dx_sign):
                self.draw_point((y0, x), type=type)
        elif dx == 0:
            for y in range(y0, y1, dy_sign):
                self.draw_point((y, start[1]), type=type)
        else:
            slope = dy/dx
            if dy>dx:
                xx = 0
                for x in range(x0, x1+1, dx_sign):
                    for y in range(y0+xx*slope, y1+(xx+1)*slope, dy_sign):
                        self.draw_point((y,x), type=type)
                    xx += 1
            elif dx>dy:
                yy = 0
                for y in range(y0, y1+1, dy_sign):
                    for x in range(x0+yy/slope, x1+(yy+1)/slope, dx_sign):
                        self.draw_point((y,x), type=type)
    
    def draw_shape(self, points, closed=False, type='wall'):
        for ii in range(len(points)-1):
            self.draw_line(points[ii], points[ii+1], type=type)
        if closed:
            self.draw_line(points[-1], points[0], type=type)
