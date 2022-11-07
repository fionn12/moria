
import pgzrun
from random import randint
from random import randrange
import pygame

GUERRERO_IZQUIERDA = 'guerrero-izqiureda4'
GUERRERO_IZQUIERDA_ATACA = 'guerrero-attackeizqiurdo1'

zombie_arriba = 'enemigo1'
zombie_abajo = 'enemigoabajo2'
zombie_derecha = 'enemigoderecha2'
zombie_izqiurdo = 'enemigoizqiurda2'



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
#OFFSET_ZOMBIE = (-55, -50)
OFFSET_ZOMBIE = (-PIXEL_WIDTH_PER_CELL*0.5, -PIXEL_HEIGHT_PER_CELL*0.5)
X_LEFT = (WIDTH - COLS * PIXEL_WIDTH_PER_CELL) / 2
Y_TOP = ( HEIGHT - ROWS * PIXEL_HEIGHT_PER_CELL) / 2
hit_zombie = False
TURN = 0

current_floor = 1
level = current_floor
max_hp = 8
current_hp = max_hp
player = Actor(GUERRERO_IZQUIERDA)
player.actor_type = 'player'
player.col = 1
player.row = 1
player.offset = OFFSET_IZQUIERDA
hart = Actor('corazon')
hart.actor_type = 'heart'
hart_negro = Actor('corazon.malo1')
hart_negro.actor_type = 'heart'
hart.pos = hart.x, hart.y
hart_negro.pos = hart_negro.x, hart_negro.y
hart.x = 300
hart.y = 850
hart_negro.x = 300
hart_negro.y = 850
puerta_abajo = Actor('escaleras-abajo1')
puerta_abajo.actor_type = 'puerta'
puerta_arriba = Actor('escaleras-arriba')
puerta_arriba.actor_type = 'puerta'
zombie = Actor(zombie_arriba)
zombie_hp = 3
zombie.backuprow = player.row
zombie.backupcol = player.col
zombie.actor_type= 'monster_zombie'


mapa = Rect(0, 0, COLS * PIXEL_WIDTH_PER_CELL, ROWS * PIXEL_HEIGHT_PER_CELL)
mapa.move_ip(X_LEFT, Y_TOP)
current_floor_indicatorbox = Rect(0, 0, 200, 100)
current_floor_indicatorbox.move_ip(400, 100)
current_cell_indicatorbox = Rect(0, 0, 200, 100)
current_floor_bob = Rect(0, 0, 200, 100)
current_floor_bob.move_ip(200, 100)
current_floor_jeff = Rect(0, 0, 200, 100)
current_floor_jeff.move_ip(800, 500)

zombie_col = 0
zombie_row = 0
zombie_newcol = zombie_col - 1
zombie_newrow = zombie_row - 1
zombie.backup_col = 0
zombie.backup_row = 0


current_cell_indicatorbox.move_ip(0, 100)

def draw():
    draw_matrix(mapa_nivel)

def draw_matrix(matrix):
    global current_hp
    screen.fill('dim grey')
    screen.draw.filled_rect(mapa, 'sky blue')
    screen.draw.filled_rect(current_floor_indicatorbox, 'orange')
    screen.draw.textbox('turn ' + str(TURN), current_floor_indicatorbox, color=('black'))
    screen.draw.textbox(str(player.col) + ',' + str(player.row), current_cell_indicatorbox, color=('black'))
    screen.draw.filled_rect(current_floor_bob, 'orange')
    screen.draw.filled_rect(current_floor_jeff, 'orange')
    screen.draw.textbox(str(zombie_hp), current_floor_jeff, color='black')
    #if hit_zombie:
        #screen.draw.textbox('Hit', current_floor_bob, color='black')
    #else:
    screen.draw.textbox(str(zombie_col) + ':' + str(zombie_row), current_floor_bob, color='black')

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ' ':
                current_cell = Rect(0, 0, PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL)
                current_cell.move_ip(X_LEFT+i*PIXEL_WIDTH_PER_CELL, Y_TOP + j * PIXEL_HEIGHT_PER_CELL)
                screen.draw.textbox(str(matrix[i][j]), current_cell, color=('black'))
            else:
                matrix[i][j].pos = (0,0)
                if matrix[i][j].actor_type =='monster_zombie':
                   matrix[i][j].move_ip(X_LEFT + i * PIXEL_WIDTH_PER_CELL + OFFSET_ZOMBIE[0], Y_TOP + j * PIXEL_HEIGHT_PER_CELL  + OFFSET_ZOMBIE[1]) 
                else:
                   matrix[i][j].move_ip(X_LEFT + (i +1) * PIXEL_WIDTH_PER_CELL + OFFSET_ZOMBIE[0], Y_TOP + (j+2) * PIXEL_HEIGHT_PER_CELL  + OFFSET_ZOMBIE[1]) 
                matrix[i][j].draw()            
            
        
    
    for row in range(1, ROWS):
        y = Y_TOP + row * PIXEL_HEIGHT_PER_CELL
        screen.draw.line((X_LEFT, y), (WIDTH - X_LEFT, y), 'azure')
    for col in range(1, COLS):
        x = X_LEFT + col * PIXEL_WIDTH_PER_CELL
        screen.draw.line((x, Y_TOP), (x, HEIGHT - Y_TOP), 'azure')

    hart.x = 300
    hart_negro.x = 300
    for teller in range(1, max_hp):
        if teller > current_hp:
            hart_negro.draw()
        else:
            hart.draw() 
        hart.x += 70
        hart_negro.x += 70
        
        

    draw_player()


def draw_player():
    player.pos = (X_LEFT + player.col * PIXEL_WIDTH_PER_CELL - PIXEL_WIDTH_PER_CELL / 2 + player.offset[0], Y_TOP + player.row  * PIXEL_HEIGHT_PER_CELL + player.offset[1])
    player.draw()




def on_key_down(key):
    global TURN, zombie_col, zombie_row, mapa_nivel
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
        player.row = player.backuprow
        player.col= player.backupcol
        on_hit()
        
      #monster_turn
      if es_impar(TURN):
          new_zombie_position = calculate_new_zombie_location(player.col, player.row, zombie_col, zombie_row)
          move_zombie(zombie_col, zombie_row, new_zombie_position[0], new_zombie_position[1])
         
      
        
    

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

def move_zombie(fromCol, fromRow, toCol, toRow):
    global mapa_nivel, zombie_col, zombie_row
    mapa_nivel[toCol][toRow] = mapa_nivel[fromCol][fromRow]
    mapa_nivel[fromCol][fromRow] = ' '
          
    zombie_col = toCol
    zombie_row = toRow


def es_impar(n):
    if int(n / 2) * 2 == n:
        return False
    return True
        

def calculate_new_zombie_location(px, py, mx, my):
    global zombie,zombie_backup_row, zombie_backup_col, zombie_col, zombie_row
    resultx = mx
    resulty = my
    deltax = abs(px - mx)
    deltay = abs(my - py)
    zombie_backup_col = zombie_col
    zombie_backup_row = zombie_row

    if deltax <= 1 and deltay < 1:
        monster_melee_attack()        
        return (resultx, resulty)
    

    if deltax > deltay:             
        if px < mx:
            resultx -= 1
            zombie.image = zombie_izqiurdo
            return (resultx, resulty)

        elif px > mx:
            resultx += 1
            zombie.image = zombie_derecha
            return (resultx, resulty)
    
    else:            
        if py < my:
            resulty -= 1
            zombie.image = zombie_arriba
        elif py > my:
            resulty += 1
            zombie.image = zombie_abajo

    if zombie_col == player.col and zombie_row == player.row:
        zombie_col = zombie_backup_col
        zombie_row = zombie_backup_row
        return (mx, my)
            
            
    return (resultx, resulty)

#def on_zombie_hit():
#    global zombie_col, zombie_row, zombie.backup_col, zombie.backup_row
#    move_zombie(zombie_col, zombie_row, zombie.backup_col, zombie.backup_row)
    

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

def heal_player(number_hp):
    global current_hp, max_hp

    current_hp += number_hp
    if current_hp > max_hp:
        current_hp = max_hp
    

def monster_melee_attack():
    global current_hp
    current_hp -= 1

    

def generate_downdoor(a):
    r = 1 + randrange(9)
    c = 1 + randrange(9)

    a[r][c] = puerta_abajo
    puerta_abajo._surf = pygame.transform.scale(puerta_abajo._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL))



def generate_updoor(m):
    r = 1 + randrange(9)
    c = 1 + randrange(9)

    puerta_arriba._surf = pygame.transform.scale(puerta_arriba._surf, (PIXEL_WIDTH_PER_CELL, PIXEL_HEIGHT_PER_CELL)) 

    m[r][c] = puerta_arriba

def generate_zombie(a):
    global zombie_col, zombie_row

    r = 1 + randrange(9)
    c = 1 + randrange(9)
    
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


