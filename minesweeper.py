from random import randint

GAME_CONTINUE = True

class Tile():
    """Used to describe a blank Tile"""
    def __init__(self):
        self.identifier = ' '
        self.label = '+'

    def __str__(self):
        return self.label

    def find_adjacent(self, tilemap, index_x, index_y):
        if isinstance(tilemap[index_x][index_y], Mine):
            return
        adjacent = 0
        for row in range(-1, 2):
            for col in range(-1, 2):
                if index_x + row >= 0 and index_y + col >= 0:
                    if index_x + row  < len(tilemap) and index_y + col < len(tilemap[0]):
                        if isinstance(tilemap[index_x + row][index_y + col], Mine):
                            adjacent += 1
        if adjacent != 0:
            tilemap[index_x][index_y] = NonMine(adjacent)

    def reveal(self):
        self.label = self.identifier

    def interact(self, tilemap, index):
        """Find all connecting empty tiles and tiles with mines next to them and reveal them"""
        if self.label == self.identifier:
            return
        self.reveal()
        for row in range(-1, 2):
            for col in range(-1, 2):
                if index[0] + row >= 0 and index[1] + col >= 0:
                    if index[0] + row  < len(tilemap) and index[1] + col < len(tilemap[0]):
                        if not (abs(row) == abs(col) and isinstance(tilemap[index[0] + row][index[1] + col]) == Tile):
                            tilemap[index[0] + row][index[1] + col].interact(tilemap, [index[0] + row, index[1] + col])

class NonMine(Tile):
    """Used to describe non-Mine Tile with adjacencies"""
    def __init__(self, adjacent):
        super().__init__()
        self.adjacent = adjacent
        self.identifier = str(adjacent)

    def interact(self, tilemap, index):
        if self.label == self.identifier:
            return
        self.reveal()

class Mine(Tile):
    """Used to describe a Mine Tile only"""
    def __init__(self):
        super().__init__()
        self.identifier = 'X'

    def interact(self, tilemap, index):
        """End game and reveal all mines"""
        global GAME_CONTINUE
        GAME_CONTINUE = False
        self.reveal()
        self.reveal_all(tilemap)
        print('Game over!')

    @staticmethod
    def reveal_all(tilemap):
        for current_row in tilemap:
            for current_tile in current_row:
                current_tile.reveal()

def tilemap_print(tilemap):
    print('  ', end='')
    for i in range(len(tilemap[0])):
        print(i, end='')
    print()

    for rows, _ in enumerate(tilemap):
        current_row = tilemap[rows]
        print(f'{rows} ', end='')
        for cols in range(len(tilemap[0])):
            print(current_row[cols], end='')
        print()
    return tilemap

def new_bomb_location(tilemap):
    row = randint(0, len(tilemap) - 1)
    col = randint(0, len(tilemap[0]) - 1)
    #if location is already a bomb
    if isinstance(tilemap[row][col], Mine):
        return new_bomb_location(tilemap)
    else:
        return row, col

def plant_bombs(tilemap, amount):
    for _ in range(amount):
        row, col = new_bomb_location(tilemap)
        tilemap[row][col] = Mine()
    return tilemap

def tilemap_create(length, width, bombs):
    tilemap = []
    for _ in range(length):
        new_row = []
        for _ in range(width):
            new_row.append(Tile())
        tilemap.append(new_row)

    tilemap = plant_bombs(tilemap, bombs)

    for count_length, current_row in enumerate(tilemap):
        for count_width, current_tile in enumerate(current_row):
            current_tile.find_adjacent(tilemap, count_length, count_width)

    return tilemap

def get_user_input():
    user = input('Enter coordinates (X,Y): ')
    if user == 'Q':
        return [-1,-1]
    user = user.split(',')
    response = [int(user[1]), int(user[0])]
    return response

def main():
    rows = 10 # max  = 10
    cols = 10 # max = 10
    bombs = 25 # max = rows * cols

    tilemap = tilemap_create(cols, rows, bombs)

    while GAME_CONTINUE:
        tilemap_print(tilemap)
        try:
            user = get_user_input()
            if user == [-1,-1]:
                break
            tilemap[user[0]][user[1]].interact(tilemap, user)
        except:
            print('Invalid input, try again')
    print('\n')
    tilemap_print(tilemap) #print last time to show result

if __name__ == '__main__':
    main()
