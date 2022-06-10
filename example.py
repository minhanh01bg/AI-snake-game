import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
HEIGHT = 10
WIDTH = 15
FIELD_SIZE = HEIGHT * WIDTH
HEAD = 0

FOOD = 0
UNDEFINED = (HEIGHT + 1) * (WIDTH + 1)
SNAKE = 2 * UNDEFINED

LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH 

ERR = -2333
MOV = [LEFT, RIGHT, UP, DOWN]

SNAKE_BLOCK = 20
SNAKE_SPEED = 200

FONT_STYLE = pygame.font.SysFont("bahnschrift", 12)
SCORE_FONT = pygame.font.SysFont("comicsansms", 20)

def initial_game():
    global board, snake, snake_size, tmpboard, tmpsnake, tmpsnake_size, food,best_move
    board = [0] * FIELD_SIZE #[0,0,0,……]
    snake = [0] * (FIELD_SIZE+1)
    snake[HEAD] = 1*WIDTH+1
    snake_size = 1

    tmpboard = [0] * FIELD_SIZE
    tmpsnake = [0] * (FIELD_SIZE+1)
    tmpsnake[HEAD] = 1*WIDTH+1
    tmpsnake_size = 1

    food = 4 * WIDTH + 7
    best_move = ERR

      
  


dis = pygame.display.set_mode((SNAKE_BLOCK*WIDTH, SNAKE_BLOCK*HEIGHT))
 
clock = pygame.time.Clock()

 

 
 
def Your_score(score):
    value = SCORE_FONT.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
def new_food():
    global food, snake_size, dis
    cell_free = False
    while not cell_free:
        w = random.randint(0, WIDTH-1)
        h = random.randint(0, HEIGHT-1)
        food = WIDTH*h + w
        cell_free = is_cell_free(food, snake_size, snake)
    
    
def draw():
    global SNAKE_BLOCK,snake,snake_size,food
    for idx in snake[:snake_size]:
        pygame.draw.rect(dis, black, [SNAKE_BLOCK*(idx%WIDTH), SNAKE_BLOCK*(idx//WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
    pygame.draw.rect(dis, green, [SNAKE_BLOCK*(food%WIDTH), SNAKE_BLOCK*(food//WIDTH), SNAKE_BLOCK, SNAKE_BLOCK])
 
 
def message(msg, color):
    mesg = FONT_STYLE.render(msg, True, color)
    dis.blit(mesg, [WIDTH*SNAKE_BLOCK / 6, HEIGHT*SNAKE_BLOCK / 3])
 
def is_move_possible(idx, move):
    flag = False
    if move == LEFT:
        flag = True if idx%WIDTH > 0 else False
    elif move == RIGHT:
        flag = True if idx%WIDTH < (WIDTH-1) else False
    elif move == UP:
        flag = True if idx > (WIDTH-1) else False
    elif move == DOWN:
        flag = True if idx < (FIELD_SIZE-WIDTH) else False
    return flag
    
def is_cell_free(idx, psize, psnake):
    return not (idx in psnake[:psize]) 
    
def board_BFS(pfood, psnake, pboard):
    queue = []
    queue.append(pfood)
    inqueue = [0] * FIELD_SIZE
    found = False
    while len(queue)!=0: 
        idx = int(queue.pop(0))
        if inqueue[idx] == 1: 
            continue
        inqueue[idx] = 1
        for i in range(4):
            if is_move_possible(idx, MOV[i]):
                if idx + MOV[i] == psnake[HEAD]:
                    found = True
                if pboard[idx+MOV[i]] < SNAKE: 
                    if pboard[idx+MOV[i]] > pboard[idx]+1:
                        pboard[idx+MOV[i]] = pboard[idx] + 1
                    if inqueue[idx+MOV[i]] == 0:
                        queue.append(idx+MOV[i])
    return found
    
def is_tail_reachable(): 
    global tmpboard, tmpsnake, food, tmpsnake_size
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD 
    tmpboard[food] = SNAKE 
    result = board_BFS(tmpsnake[tmpsnake_size-1], tmpsnake, tmpboard) 
    for i in range(4): 
        if is_move_possible(tmpsnake[HEAD], MOV[i]) and tmpsnake[HEAD]+MOV[i]==tmpsnake[tmpsnake_size-1] and tmpsnake_size>3:
            result = False
    return result

def make_move(move):
    global snake, board, snake_size, score
    shift_array(snake, snake_size)
    snake[HEAD] += move
    p = snake[HEAD]
    
    if snake[HEAD] == food:
        board[snake[HEAD]] = SNAKE 
        snake_size += 1
        if snake_size < FIELD_SIZE: new_food()
    else: 
        board[snake[HEAD]] = SNAKE 
        board[snake[snake_size]] = UNDEFINED 
    
def board_reset(psnake, psize, pboard):
    for i in range(FIELD_SIZE):
        if i == food:
            pboard[i] = FOOD
        elif is_cell_free(i, psize, psnake): 
            pboard[i] = UNDEFINED
        else:
            pboard[i] = SNAKE
            
def find_safe_way():
    global snake, board
    safe_move = ERR
    virtual_shortest_move() 
    if is_tail_reachable(): 
        return choose_shortest_safe_move(snake, board)
    safe_move = follow_tail()
    return safe_move
    
def shift_array(arr, size):
    for i in range(size, 0, -1):
        arr[i] = arr[i-1]
        
def any_possible_move():
    global food , snake, snake_size, board
    best_move = ERR
    board_reset(snake, snake_size, board)
    board_BFS(food, snake, board)
    min = SNAKE

    for i in range(4):
        if is_move_possible(snake[HEAD], MOV[i]) and board[snake[HEAD]+MOV[i]]<min:
            min = board[snake[HEAD]+MOV[i]]
            best_move = MOV[i]
    return best_move
    
def follow_tail():
    global tmpboard, tmpsnake, food, tmpsnake_size
    tmpsnake_size = snake_size
    tmpsnake = snake[:]
    board_reset(tmpsnake, tmpsnake_size, tmpboard) 
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD
    tmpboard[food] = SNAKE
    board_BFS(tmpsnake[tmpsnake_size-1], tmpsnake, tmpboard) 
    tmpboard[tmpsnake[tmpsnake_size-1]] = SNAKE 
    return choose_longest_safe_move(tmpsnake, tmpboard) 
    
def virtual_shortest_move():
    global snake, board, snake_size, tmpsnake, tmpboard, tmpsnake_size, food
    tmpsnake_size = snake_size
    tmpsnake = snake[:] 
    tmpboard = board[:] 
    board_reset(tmpsnake, tmpsnake_size, tmpboard)
    
    food_eated = False
    while not food_eated:
        board_BFS(food, tmpsnake, tmpboard)    
        move = choose_shortest_safe_move(tmpsnake, tmpboard)
        shift_array(tmpsnake, tmpsnake_size)
        tmpsnake[HEAD] += move 
        if tmpsnake[HEAD] == food:
            tmpsnake_size += 1
            board_reset(tmpsnake, tmpsnake_size, tmpboard)
            tmpboard[food] = SNAKE
            food_eated = True
        else:
            tmpboard[tmpsnake[HEAD]] = SNAKE
            tmpboard[tmpsnake[tmpsnake_size]] = UNDEFINED
            
def choose_shortest_safe_move(psnake, pboard):
    best_move = ERR
    min = SNAKE
    for i in range(4):
        if is_move_possible(psnake[HEAD], MOV[i]) and pboard[psnake[HEAD]+MOV[i]]<min:
            min = pboard[psnake[HEAD]+MOV[i]]
            best_move = MOV[i]
    return best_move
    
def choose_longest_safe_move(psnake, pboard):
    best_move = ERR
    max = -1
    for i in range(4):
        if is_move_possible(psnake[HEAD], MOV[i]) and pboard[psnake[HEAD]+MOV[i]]<UNDEFINED and pboard[psnake[HEAD]+MOV[i]]>max:
            max = pboard[psnake[HEAD]+MOV[i]]
            best_move = MOV[i]
    return best_move

def gameLoop():
    game_over = False
    game_close = False
 
    initial_game()
 
    while not game_over:
        
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(snake_size - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
        
        board_reset(snake, snake_size, board)
        
        if board_BFS(food, snake, board):
            best_move  = find_safe_way()
        else:
            best_move = follow_tail()
        if best_move == ERR:
            best_move = any_possible_move()
            
        if best_move != ERR: 
            make_move(best_move)
        else:
            game_close = True
        
        dis.fill(blue)
        
        draw()
        Your_score(snake_size - 1)
 
        pygame.display.update()
 
        clock.tick(SNAKE_SPEED)
 
    pygame.quit()
    quit()
 
 
gameLoop()