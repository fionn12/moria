import pgzrun
from random import randint
from random import randrange

COLS = 10
ROWS = 10
PIXEL_WIDTH_PER_CELL = 50
PIXEL_HEIGHT_PER_CELL = 50
HEIGHT = 1000
WIDTH = 1000
OFFSET_DERECHA = (PIXEL_WIDTH_PER_CELL * 0.5 , -PIXEL_HEIGHT_PER_CELL * 0.5);
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
hart.pos = hart.x, hart.y
hart.x = 300
hart.y = 850
puerta_abajo = Actor('escaleras-abajo1')
puerta_arriba = Actor('escaleras-arriba')

mapa = Rect(0, 0, COLS * PIXEL_WIDTH_PER_CELL, ROWS * PIXEL_HEIGHT_PER_CELL)
mapa.move_ip(X_LEFT, Y_TOP)
current_floor_indicatorbox = Rect(0, 0, 200, 100)
current_floor_indicatorbox.move_ip(400, 100)
current_cell_indicatorbox = Rect(0, 0, 200, 100)
current_cell_indicatorbox.move_ip(100, 100)

def draw():
    draw_matrix(mapa_nivel)

def draw_matrix(matrix):
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
                matrix[i][j].move_ip(X_LEFT+i*PIXEL_WIDTH_PER_CELL, Y_TOP + j * PIXEL_HEIGHT_PER_CELL)
                matrix[i][j].draw()            
            
        
    
    for row in range(1, ROWS):
        y = Y_TOP + row * PIXEL_HEIGHT_PER_CELL
        screen.draw.line((X_LEFT, y), (WIDTH - X_LEFT, y), 'azure')
    for col in range(1, COLS):
        x = X_LEFT + col * PIXEL_WIDTH_PER_CELL
        screen.draw.line((x, Y_TOP), (x, HEIGHT - Y_TOP), 'azure')

    hart.x = 300
    for teller in range(1, max_hp):
        hart.draw() 
        hart.x += 70

    draw_player()


def draw_player():
    player.pos = (X_LEFT + player.col * PIXEL_WIDTH_PER_CELL - PIXEL_WIDTH_PER_CELL / 2 + player.offset[0], Y_TOP + player.row  * PIXEL_HEIGHT_PER_CELL + player.offset[1])

    player.draw()

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

def generate_map(rows, cols):
    Matrix = [[' ' for x in range(cols)] for y in range(rows)]

    Matrix[randrange(9)][randrange(9)] = puerta_abajo
    
    return Matrix
    


mapa_nivel = generate_map(10,10)

    

    


pgzrun.go()


