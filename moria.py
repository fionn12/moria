import pgzrun
from random import randint
from random import randrange
import pygame


COLS = 10
ROWS = 10
PIXEL_WIDTH_PER_CELL = 50
PIXEL_HEIGHT_PER_CELL = 50
HEIGHT = 1000
WIDTH = 1000
OFFSET_DERECHA = (PIXEL_WIDTH_PER_CELL * 0.5 , -PIXEL_HEIGHT_PER_CELL * 0.5)
OFFSET_ABAJO = (0, 0)
OFFSET_ARRIBA = (0, -PIXEL_HEIGHT_PER_CELL)
OFFSET_IZQUIERDA= (-PIXEL_WIDTH_PER_CELL*0.5, -PIXEL_HEIGHT_PER_CELL * 0.5)
X_LEFT = (WIDTH - COLS * PIXEL_WIDTH_PER_CELL) / 2
Y_TOP = ( HEIGHT - ROWS * PIXEL_HEIGHT_PER_CELL) / 2



current_floor = 1
level = current_floor
max_hp = 8
player = Actor('guerrero-izqiureda4')
player.col = 1
player.row = 1
player.offset = OFFSET_IZQUIERDA

hart = Actor('corazon')
hart.col = 300
hart.row = 850
hart.pos = hart.col, hart.row


puerta_arriba = Actor('escaleras-arriba')


actors_dictionary = {
    "player" : { "actor": player, 
                 "max_hp": 8
               }
}

maze_levels = []


mapa = Rect(0, 0, COLS * PIXEL_WIDTH_PER_CELL, ROWS * PIXEL_HEIGHT_PER_CELL)
mapa.move_ip(X_LEFT, Y_TOP)
current_floor_indicatorbox = Rect(0, 0, 200, 100)
current_floor_indicatorbox.move_ip(400, 100)
current_cell_indicatorbox = Rect(0, 0, 200, 100)

current_cell_indicatorbox.move_ip(100, 100)

def draw():
    draw_matrix(current_floor)

def draw_matrix(level):
    matrix = maze_levels [level - 1]
    screen.fill('dim grey')
    screen.draw.filled_rect(mapa, 'sky blue')
    screen.draw.filled_rect(current_floor_indicatorbox, 'orange')
    screen.draw.textbox('your level is: ' + str(current_floor), current_floor_indicatorbox, color=('black'))
    screen.draw.textbox('Row: ' + str(player.row) + ', col:' + str(player.col), current_cell_indicatorbox, color=('black'))

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ' ':
                current_cell = Rect(0, 0, PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL)
                current_cell.move_ip(X_LEFT+i*PIXEL_WIDTH_PER_CELL, Y_TOP + j * PIXEL_HEIGHT_PER_CELL)
                screen.draw.textbox(str(matrix[i][j]), current_cell, color=('black'))
            else:
                matrix[i][j].draw()            
            
        
    
    for row in range(1, ROWS):
        y = Y_TOP + row * PIXEL_HEIGHT_PER_CELL
        screen.draw.line((X_LEFT, y), (WIDTH - X_LEFT, y), 'azure')
    for col in range(1, COLS):
        x = X_LEFT + col * PIXEL_WIDTH_PER_CELL
        screen.draw.line((x, Y_TOP), (x, HEIGHT - Y_TOP), 'azure')

   
    hart.col = 300
    hart.pos = hart.col, hart.row
    for teller in range(1, max_hp):
        hart.draw() 
        hart.col += 70
        hart.pos = hart.col, hart.row

    draw_actor("player")


def draw_actor(name):
    thisactor = actors_dictionary[name]["actor"]

    thisactor.pos = (X_LEFT + thisactor.col * PIXEL_WIDTH_PER_CELL - PIXEL_WIDTH_PER_CELL / 2 + thisactor.offset[0], Y_TOP + thisactor.row  * PIXEL_HEIGHT_PER_CELL + thisactor.offset[1])
    thisactor.draw()


def on_key_down(key):
    if key == keys.UP:
        player.row -= 1
        player.image = 'guerrero-1bien'
        player.offset = OFFSET_ARRIBA
    elif key == keys.RIGHT:
        player.col += 1
        player.image = 'guerrero-derecha3'
        player.offset = OFFSET_DERECHA 
    elif key == keys.LEFT:
        player.col -= 1
        player.image = 'guerrero-izqiureda4'
        player.offset = OFFSET_IZQUIERDA
    elif key == keys.DOWN:
        player.row += 1
        player.image = 'guerrero-abago'
        player.offset = OFFSET_ABAJO

    if player.row < 1:
        player.row = 1
        
    if player.row >= ROWS:
        player.row = ROWS

    if player.col < 1:
        player.col = 1

    if player.col >= COLS:
        player.col = COLS

    return


def generate_door(nivel, m, name, sprite):
    r = randrange(9)
    c = randrange(9)

    actorname = name + "_" + str(nivel)
    actors_dictionary[actorname] = {
        "actor" : Actor(sprite),
        "offset" : (0,0)
    }
    
    m[r][c] = actors_dictionary[actorname]["actor"] 
    actors_dictionary[actorname]["actor"] ._surf = pygame.transform.scale(actors_dictionary[actorname]["actor"] ._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL))
    actors_dictionary[actorname]["actor"] .move_ip(X_LEFT+r*PIXEL_WIDTH_PER_CELL, Y_TOP + c * PIXEL_HEIGHT_PER_CELL)

def generate_updoor(a):
    r = randrange(9)
    c = randrange(9)

    puerta_arriba._surf = pygame.transform.scale(puerta_arriba._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL)) 
    puerta_arriba.move_ip(X_LEFT+r*PIXEL_WIDTH_PER_CELL, Y_TOP + c * PIXEL_HEIGHT_PER_CELL) 

    a[r][c] = puerta_arriba

def generate_map(level, rows, cols):
    Matrix = [[' ' for x in range(cols)] for y in range(rows)]

    generate_door(level, Matrix, 'abajo', 'escaleras-abajo1')
    generate_door(level, Matrix, 'arriba', 'escaleras-arriba')
     
    return Matrix

    

maze_levels.append(generate_map(1, 10,10))
maze_levels.append(generate_map(2, 10,10))
    


pgzrun.go()


