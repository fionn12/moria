import pgzrun
from random import randint
from random import randrange
import pygame

GUERRERO_IZQUIERDA = 'guerrero-izqiureda4'
GUERRERO_IZQUIERDA_ATACA= 'guerrero-attackeizqiurdo1'


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
OFFSET_ZOMBIE = (-55, -50)
X_LEFT = (WIDTH - COLS * PIXEL_WIDTH_PER_CELL) / 2
Y_TOP = ( HEIGHT - ROWS * PIXEL_HEIGHT_PER_CELL) / 2
hit_zombie = False
TURN = 0

current_floor = 1
level = current_floor
max_hp = 8
player = Actor(GUERRERO_IZQUIERDA)
player.col = 1
player.row = 1
player.offset = OFFSET_IZQUIERDA
hart = Actor('corazon')
hart.pos = hart.x, hart.y
hart.x = 300
hart.y = 850
puerta_abajo = Actor('escaleras-abajo1')
puerta_arriba = Actor('escaleras-arriba')
zombie = Actor('enemigo1')
zombie_abajo = Actor('enemigoabajo')
zombie_derecha = Actor('enemigoderecha')
zombie_izqiurdo = Actor('enemigoizqiurda')
zombie_hp = 3
player.backuprow = player.row
player.backupcol = player.col


mapa = Rect(0, 0, COLS * PIXEL_WIDTH_PER_CELL, ROWS * PIXEL_HEIGHT_PER_CELL)
mapa.move_ip(X_LEFT, Y_TOP)
current_floor_indicatorbox = Rect(0, 0, 200, 100)
current_floor_indicatorbox.move_ip(400, 100)
current_cell_indicatorbox = Rect(0, 0, 200, 100)
current_floor_bob = Rect(0, 0, 200, 100)
current_floor_bob.move_ip(200, 100)

zombie_col = 0
zombie_row = 0
zombie_newcol = zombie_col - 1
zombie_newrow = zombie_row



current_cell_indicatorbox.move_ip(100, 100)

def draw():
    draw_matrix(mapa_nivel)

def draw_matrix(matrix):
    screen.fill('dim grey')
    screen.draw.filled_rect(mapa, 'sky blue')
    screen.draw.filled_rect(current_floor_indicatorbox, 'orange')
    screen.draw.textbox('your level is: ' + str(current_floor), current_floor_indicatorbox, color=('black'))
    screen.draw.textbox('Row: ' + str(player.row) + ', col:' + str(player.col), current_cell_indicatorbox, color=('black'))
    screen.draw.filled_rect(current_floor_bob, 'orange')
    if hit_zombie:
        screen.draw.textbox('Hit', current_floor_bob, color='black')
    else:
        screen.draw.textbox(str(TURN) + ' ' + str(zombie_col) + 'z' + str(zombie_row), current_floor_bob, color='black')

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

    hart.x = 300
    for teller in range(1, max_hp):
        hart.draw() 
        hart.x += 70

    draw_player()


def draw_player():
    player.pos = (X_LEFT + player.col * PIXEL_WIDTH_PER_CELL - PIXEL_WIDTH_PER_CELL / 2 + player.offset[0], Y_TOP + player.row  * PIXEL_HEIGHT_PER_CELL + player.offset[1])

    player.draw()




def on_key_down(key):
    global TURN
    global zombie_col
    global zombie_row, mapa_nivel
    increase_turn = False

    player.backuprow = player.row
    player.backupcol = player.col

    
    if key == keys.UP:
        player.row -= 1
        player.image = 'guerrero-1bien'
        player.offset = OFFSET_ARRIBA
        increase_turn = True
        
    elif key == keys.RIGHT:
        player.col += 1
        player.image = 'guerrero-derecha3'
        player.offset = OFFSET_DERECHA
        increase_turn = True
    elif key == keys.LEFT:
        player.col -= 1
        player.image = GUERRERO_IZQUIERDA
        player.offset = OFFSET_IZQUIERDA
        increase_turn = True
    elif key == keys.DOWN:
        player.row += 1
        player.image = 'guerrero-abago'
        player.offset = OFFSET_ABAJO
        increase_turn = True
       

    if increase_turn == True:
      TURN += 1
      if zombie_col == player.col and zombie_row == player.row:
        on_hit()
      #monster_turn
      new_zombie_position = calculate_new_zombie_location(player.col, player.row, zombie_col, zombie_row)
      mapa_nivel[new_zombie_position[0]][new_zombie_position[1]] = mapa_nivel[zombie_col][zombie_row]
      mapa_nivel[zombie_col][zombie_row] = ' '
      
      zombie_col = new_zombie_position[0]
      zombie_row = new_zombie_position[1]
      
        
    

    if player.row < 1:
        player.row = 1
        increase_turn = False        
    if player.row >= ROWS:

        player.row = ROWS
        increase_turn = False
    if player.col < 1:
        player.col = 1
        increase_turn = False
    if player.col >= COLS:
        player.col = COLS
        increase_turn = False

  

def calculate_new_zombie_location(px, py, mx, my):
    resultx = mx
    resulty = my
    
    if px < mx:
        resultx -= 1
        zombie.move_ip(-PIXEL_WIDTH_PER_CELL, 0)
        return (resultx, resulty)

    elif px > mx:
        resultx += 1
        zombie.move_ip(PIXEL_WIDTH_PER_CELL, 0)
        return (resultx, resulty)

    if py < my:
        resulty -= 1
        zombie.move_ip(0, -PIXEL_HEIGHT_PER_CELL)

    elif py > my:
        resulty += 1
        zombie.move_ip(0, PIXEL_HEIGHT_PER_CELL)
        
    return (resultx, resulty)


def on_hit():
    global hit_zombie

    hit_zombie = True
    
    if player.image == 'guerrero-1bien':
        player.image = 'guerrero-attacke'
        
    if player.image == 'guerrero-derecha3':
        player.image = 'guerrero-attackederecha2'
        
    if player.image == GUERRERO_IZQUIERDA:
        player.image = GUERRERO_IZQUIERDA_ATACA
        
    if player.image == 'guerrero-abago':
        player.image = 'guerrero-attackeabajo1'

    player.row = player.backuprow
    player.col = player.backupcol
        

def generate_downdoor(m):
    r = randrange(9)
    c = randrange(9)

    m[r][c] = puerta_abajo
    puerta_abajo._surf = pygame.transform.scale(puerta_abajo._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL))


    puerta_abajo.move_ip(X_LEFT+r*PIXEL_WIDTH_PER_CELL, Y_TOP + c * PIXEL_HEIGHT_PER_CELL)

def generate_updoor(a):
    r = randrange(9)
    c = randrange(9)

    puerta_arriba._surf = pygame.transform.scale(puerta_arriba._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL)) 
    puerta_arriba.move_ip(X_LEFT+r*PIXEL_WIDTH_PER_CELL, Y_TOP + c * PIXEL_HEIGHT_PER_CELL) 

    a[r][c] = puerta_arriba

def generate_zombie(a):
    global zombie_col, zombie_row

    r = randrange(9)
    c = randrange(9)
    

    #zombie._surf = pygame.transform.scale(zombie._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL)) 
    zombie.move_ip(X_LEFT + c * PIXEL_WIDTH_PER_CELL + OFFSET_ZOMBIE[0], Y_TOP + r * PIXEL_HEIGHT_PER_CELL  + OFFSET_ZOMBIE[1]) 

    #zombie.pos = (r,c)
    a[c][r] = zombie
    zombie_col = c
    zombie_row = r

def generate_map(rows, cols):
    Matrix = [[' ' for x in range(cols)] for y in range(rows)]

    generate_downdoor(Matrix)
    generate_updoor(Matrix)
    generate_zombie(Matrix)
        
    return Matrix

# def new_floor():
#     if player.collidepoint(puerta_abajo):
#     pass
    


mapa_nivel = generate_map(10,10)

    

    


pgzrun.go()


