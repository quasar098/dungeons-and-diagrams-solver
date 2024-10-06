EMPTY = 0
MONSTER = 1
CHEST = 2
WALL = 3
UNKNOWN = 4

SIZE = 8


class State:
    def __init__(self):
        self.rows = []
        self.col_nums = []
        self.row_nums = []
        self.monster_positions = []
        self.chest_positions = []
        for _ in range(SIZE):
            self.rows.append([UNKNOWN] * SIZE)

    def copy(self):
        state = State()
        state.rows = [row.copy() for row in self.rows]
        state.col_nums = self.col_nums.copy()
        state.row_nums = self.row_nums.copy()
        state.monster_positions = self.monster_positions
        state.chest_positions = self.chest_positions
        return state

    @staticmethod
    def from_string(bs: str):
        state = State()
        translate = {'?': UNKNOWN, '@': CHEST, '!': MONSTER}
        top_row, *string_rows = [s.strip(' ') for s in bs.strip().splitlines()]
        state.col_nums = [int(i) for i in top_row]
        assert len(top_row) == SIZE, f'top row needs to be {SIZE} long'
        assert len(string_rows) == SIZE, f'string rows needs to be {SIZE} long'
        for i, row in enumerate(string_rows):
            state.row_nums.append(int(row[0]))
            assert len(row) == SIZE+1, f"row {i+1} needs to be {SIZE} long"
            for j, tile in enumerate(row[1:]):
                state.rows[i][j] = translate[tile]
                if MONSTER == translate[tile]:
                    state.monster_positions.append((j, i))
                elif CHEST == translate[tile]:
                    state.chest_positions.append((j, i))
        return state

    def __repr__(self):
        total = []
        translate = {EMPTY: '.', UNKNOWN: '?', CHEST: '@', MONSTER: '!', WALL: "#"}
        for row in self.rows:
            total.append(''.join(translate[c] for c in row))
        return '\n'.join(total)

    def check_valid(self):
        # sanity check
        for i in range(SIZE):
            if all(tile != UNKNOWN for tile in self.rows[i]):
                if sum(tile == WALL for tile in self.rows[i]) != self.row_nums[i]:
                    return False
            else:
                if sum(tile == WALL for tile in self.rows[i]) > self.row_nums[i]:
                    return False
        for i in range(SIZE):
            if all(row[i] != UNKNOWN for row in self.rows):
                if sum(row[i] == WALL for row in self.rows) != self.col_nums[i]:
                    return False
            else:
                if sum(row[i] == WALL for row in self.rows) > self.col_nums[i]:
                    return False

        # check that monsters have one empty next to them
        offset_map = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for mx, my in self.monster_positions:
            unknowns_found = 0
            empties_found = 0
            for ox, oy in offset_map:
                nx, ny = mx+ox, my+oy
                if not (0 <= nx < SIZE):
                    continue
                if not (0 <= ny < SIZE):
                    continue
                if self.rows[ny][nx] == EMPTY:
                    empties_found += 1
                if self.rows[ny][nx] == UNKNOWN:
                    unknowns_found += 1
            if empties_found > 1:
                return False
            if unknowns_found == 0 and empties_found != 1:
                return False

        # check for 2x2 empties
        for x in range(7):  # todo fix for chests
            for y in range(7):
                continue_outer = False
                for cx, cy in self.chest_positions:
                    if x-3 < cx < x+4 and y-3 < cy < y+4:
                        continue_outer = True
                        break
                if continue_outer:
                    continue
                if all([self.rows[y][x] == EMPTY, self.rows[y+1][x] == EMPTY,
                        self.rows[y][x+1] == EMPTY, self.rows[y+1][x+1] == EMPTY]):
                    return False

        # check for dead ends
        for x in range(8):
            for y in range(8):
                if self.rows[y][x] != EMPTY:
                    continue
                walls_found = 0
                for ox, oy in offset_map:
                    nx, ny = x+ox, y+oy
                    if not (0 <= nx < SIZE):
                        walls_found += 1
                        continue
                    if not (0 <= ny < SIZE):
                        walls_found += 1
                        continue
                    v = self.rows[ny][nx]
                    if v == UNKNOWN:
                        continue
                    if v == WALL:
                        walls_found += 1
                if walls_found == 3:
                    return False

        # check for treasure chests
        # todo

        return True


def solve(init_state: State, depth: int = 0):
    if depth == SIZE*SIZE:
        print(init_state)
        print('=======')
        return False
    if init_state.rows[depth % SIZE][depth // SIZE] == UNKNOWN:
        wall_state = init_state.copy()
        wall_state.rows[depth % SIZE][depth // SIZE] = WALL
        if wall_state.check_valid():
            if solve(wall_state, depth+1):
                return True
        empty_state = init_state.copy()
        empty_state.rows[depth % SIZE][depth // SIZE] = EMPTY
        if empty_state.check_valid():
            if solve(empty_state, depth+1):
                return True
    else:
        solve(init_state, depth+1)


def main():
    # room 99290154
    board = """
     72624053
    2?!??????
    3???????!
    4?!????!?
    5????????
    4!??????!
    1????????
    5?!?????!
    5???!????
    """
    init_state = State.from_string(board)
    solve(init_state)


if __name__ == '__main__':
    main()
