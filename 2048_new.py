import pygame
import random
import math

pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((500, 300))
pygame.display.set_caption("2048")


class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    pygame.display.update()


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, napravlenie):
    def move_left():
        rez = [lambda x: x.col, False, (-MOVE_VEL, 0), lambda tile: tile.col == 0,
               lambda tile: tiles.get(f"{tile.row}{tile.col - 1}"),
               lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL, (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ), True]
        return rez

    def move_right():
        rez = [lambda x: x.col, True, (MOVE_VEL, 0), lambda tile: tile.col == COLS - 1,
               lambda tile: tiles.get(f"{tile.row}{tile.col + 1}"),
               lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL, (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ), False]
        return rez

    def move_up():
        rez = [lambda x: x.row, False, (0, -MOVE_VEL), lambda tile: tile.row == 0,
               lambda tile: tiles.get(f"{tile.row - 1}{tile.col}"),
               lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL, (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ), True]
        return rez

    def move_down():
        rez = [lambda x: x.row, True, (0, MOVE_VEL), lambda tile: tile.row == ROWS - 1,
               lambda tile: tiles.get(f"{tile.row + 1}{tile.col}"),
               lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL, (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ), False]
        return rez

    updated = True
    blocks = set()

    if napravlenie == "left":
        functions = move_left()
        sort_func = functions[0]
        reverse = functions[1]
        delta = functions[2]
        boundary_check = functions[3]
        get_next_tile = functions[4]
        merge_check = functions[5]
        move_check = functions[6]
        ceil = functions[7]
    elif napravlenie == "right":
        functions = move_right()
        sort_func = functions[0]
        reverse = functions[1]
        delta = functions[2]
        boundary_check = functions[3]
        get_next_tile = functions[4]
        merge_check = functions[5]
        move_check = functions[6]
        ceil = functions[7]
    elif napravlenie == "up":
        functions = move_up()
        sort_func = functions[0]
        reverse = functions[1]
        delta = functions[2]
        boundary_check = functions[3]
        get_next_tile = functions[4]
        merge_check = functions[5]
        move_check = functions[6]
        ceil = functions[7]
    elif napravlenie == "down":
        functions = move_down()
        sort_func = functions[0]
        reverse = functions[1]
        delta = functions[2]
        boundary_check = functions[3]
        get_next_tile = functions[4]
        merge_check = functions[5]
        move_check = functions[6]
        ceil = functions[7]

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


'''def checkCell(board, i, j):
    move_i = []
    move_j = []
    board_size = len(board)
    if i > 0:
        move_i.append(-1)
        move_j.append(0)
    if i < (board_size - 1):
        move_i.append(1)
        move_j.append(0)
    if j > 0:
        move_j.append(-1)
        move_i.append(0)
    if j < (board_size - 1):
        move_j.append(1)
        move_i.append(0)
    for k in range(len(move_i)):
        if board[i + move_i[k]][j + move_j[k]] == board[i][j]:
            return True
    return False


def canMove(board):

    board_size = len(board)
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                return True
            if checkCell(board, i, j):
                return True
    return False


def checkLose(board):
    nozero = False

    for elt in board:
        nozero = nozero or ("0" in elt)

    if not nozero:
        return not canMove(board)
    return False
'''

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def terminate():
    pygame.quit()
    # sys.exit()


def start_screen(screen, clock):
    global COLS
    global ROWS
    intro_text = ["Приветствую!!!", "",
                  "Сейчас игровое поле 4x4",
                  "Но ты можешь поменять его размер,",
                  "для этого нажми:",
                  "1 - для поля 3х3",
                  "2 - для поля 5х5",
                  "3 - для поля 6х6",
                  "и просто кликни мышью, чтобы начать:)"]

    fon = pygame.transform.scale(pygame.image.load('white.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
            elif event.type == pygame.KEYDOWN:
                if event.key == 49:
                    ROWS = 3
                    COLS = 3
                elif event.key == 50:
                    ROWS = 5
                    COLS = 5
                elif event.key == 51:
                    ROWS = 6
                    COLS = 6
        pygame.display.flip()
        #print(ROWS, COLS)
        clock.tick(FPS)


def end_screen(screen, clock):
    global COLS
    global ROWS
    global WINDOW
    intro_text = ["ПОТРАЧЕНО(((", "",
                  "нажми на кнопку мыши, чтобы начать заново"]

    fon = pygame.transform.scale(pygame.image.load('white.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                WINDOW = pygame.display.set_mode((500, 300))
                ROWS = 4
                COLS = 4
                main(WINDOW)
                return  None
        pygame.display.flip()
        clock.tick(FPS)


def main(window):
    global WINDOW
    global RECT_HEIGHT
    global RECT_WIDTH
    clock = pygame.time.Clock()
    run = True

    start_screen(window, clock)
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    RECT_HEIGHT = HEIGHT // ROWS
    RECT_WIDTH = WIDTH // COLS

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                can_move = ''
                if event.key == pygame.K_LEFT:
                    can_move = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    can_move = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    can_move = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    can_move = move_tiles(window, tiles, clock, "down")
                print(can_move)
                if can_move == 'lost':
                    end_screen(WINDOW, clock)
        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
