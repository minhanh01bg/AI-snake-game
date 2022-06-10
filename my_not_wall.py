
import pygame

import sys
import copy
import random


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRIDSIZE = 20  # kick thuoc moi o
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
YELLOW = (255, 255, 0)
BFSPath = (0, 255, 0)
WHITE=(255,255,255)
GREEN = (  0, 255,   0)
RED=(255,0,0)
BLUE  = (  0,   0, 255)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)



def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            # if (x + y) % 2 == 0:
            r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, (54, 54, 54), r)
            pygame.draw.rect(surface, (169, 201, 153), r,3)
            pygame.draw.rect(surface, (54, 54, 54), r,1)
                
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH)/2, (SCREEN_HEIGHT)/2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)

    def get_head_position(self):
        return self.positions[0]
    def get_ass_position(self):
        return self.positions[-1]
    
    def turn(self, point):  # direction
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x*GRIDSIZE,
               cur[1]+y*GRIDSIZE)
        # đầu con rắn bị trùng với thân của nó
        if  new in self.positions[1:] and (new[0]>= SCREEN_WIDTH or new[1] >= SCREEN_HEIGHT or new[0] < 0 or new[1] < 0):
            self.reset()
            # pass
        else:
            self.positions.insert(0, new)  # insert vào top
            if len(self.positions) > self.length:  # thêm vào đầu bớt ở cuối
                self.positions.pop()
                
    def any_possible_move(self):
        cur = self.get_head_position()
        val = random.randint(0,3)
        trans = [UP,DOWN,LEFT,RIGHT]
        x = trans[val][0]
        y = trans[val][1]        
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )

        if new not in self.positions and (new[0] <SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >= 0):
            if trans[val] == UP:
                self.turn(UP)
            if trans[val] == DOWN:
                self.turn(DOWN)
            if trans[val] == RIGHT:
                self.turn(RIGHT)
            if trans[val] == LEFT:
                self.turn(LEFT)
            return True
        
        return False
    
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH)/2, (SCREEN_HEIGHT)/2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):  # draw snake thân
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, WHITE, r)
            pygame.draw.rect(surface, RED, r, 1)  # border
            
    def draw_fake(self, surface):  # draw snake thân
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, RED, r)
            pygame.draw.rect(surface, WHITE, r, 1)  # border
            
    def draw_head(self,surface):
        snakeSurface = pygame.Surface((GRIDSIZE, GRIDSIZE))
        pygame.draw.circle(snakeSurface,WHITE, (4, 6), 2)
        pygame.draw.circle(snakeSurface, WHITE, (16, 6), 2)
        surface.blit(snakeSurface,self.positions[0])
        
    def draw_ass(self,surface):
        snakeSurface = pygame.Surface((GRIDSIZE, GRIDSIZE))
        pygame.draw.circle(snakeSurface,RED, (4, 6), 5)
        pygame.draw.circle(snakeSurface, RED, (16, 6), 5)
        surface.blit(snakeSurface,self.positions[-1])
    
    
    def handle_keys(self):  # di chuyen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    def handle(self, dir):
        if dir == 'u':
            self.turn(UP)
        elif dir == 'd':
            self.turn(DOWN)
        elif dir == 'l':
            self.turn(LEFT)
        elif dir == 'r':
            self.turn(RIGHT)
            
    def postition_list(self):
        return self.positions

    def reload_positions(self,positions_load):
        self.positions = copy.deepcopy(positions_load)

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (233, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1)*GRIDSIZE,
                         random.randint(0, GRID_HEIGHT-1)*GRIDSIZE)
    
    def check_position(self,snake):
        while self.position in snake.positions:
            self.position = (random.randint(0, GRID_WIDTH-1)*GRIDSIZE,
                         random.randint(0, GRID_HEIGHT-1)*GRIDSIZE)            

    def draw(self, surface):
        r = pygame.Rect(
            (self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)  # border

def bfs(food, snake, surface, prev):
    queue = []
    queue.append(snake.get_head_position())
    found = False
    list = []
    list.append(snake.get_head_position())
    while len(queue) != 0:
        idx = queue.pop(0)
        cur = idx
        x = UP[0]
        y = UP[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list and (new[0]<SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >=0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1:tePoint2})
            queue.append(new)
            list.append(new)

        x = DOWN[0]
        y = DOWN[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list and (new[0]<SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >=0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)

        x = LEFT[0]
        y = LEFT[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list and (new[0] < SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >= 0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            queue.append(new)   
            list.append(new)

        x = RIGHT[0]
        y = RIGHT[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list and (new[0] <SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >= 0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)

    return found

def bfs_check(food, snake, surface, prev):
    queue = []
    queue.append(snake.get_head_position())
    found = False
    list = []
    list.append(snake.get_head_position())
    while len(queue) != 0:
        idx = queue.pop(0)
        cur = idx
        x = UP[0]
        y = UP[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1: tePoint2})
            found = True
            # return True
        if new not in snake.positions[0:] and new not in list and (new[0]<SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >=0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1:tePoint2})
            queue.append(new)
            list.append(new)

        x = DOWN[0]
        y = DOWN[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            found = True
            # return True
        if new not in snake.positions[0:] and new not in list and (new[0]<SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >=0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)

        x = LEFT[0]
        y = LEFT[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            found = True
            # return True
        if new not in snake.positions[0:] and new not in list and (new[0] < SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >= 0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            queue.append(new)   
            list.append(new)

        x = RIGHT[0]
        y = RIGHT[1]
        new = (((cur[0] + (x*GRIDSIZE))),
               (cur[1]+(y*GRIDSIZE)) )
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            found = True
            # return True
        if new not in snake.positions[0:] and new not in list and (new[0] <SCREEN_WIDTH and new[1] < SCREEN_HEIGHT and new[0] >= 0 and new[1] >= 0):
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)

    return found


# clock = pygame.time.Clock()
# FPS = 30

           
    
def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    # myfont = pygame.font.SysFont('monospace', 16)
    # drawGrid(surface)
    snake = Snake()
    food = Food()
    FPS = 200
    score = 1
    
    while True:
        list_po = copy.deepcopy(snake.postition_list())
        dir_begin = copy.deepcopy(snake.direction)
        # snake.handle_keys()
        prev = {}
        answer =bfs(food, snake, surface, prev) 
        check = False
        if answer == True:
            snakeHead = (int(snake.get_head_position()[0]), int(snake.get_head_position()[1]))
            foodPosition = (int(food.position[0]), int(food.position[1]))
            tePoint = prev.get(foodPosition)
            path = []
            while foodPosition != snakeHead:
                path.append(foodPosition)
                foodPosition = tePoint
                if foodPosition is None:
                    break
                # print(foodPosition)
                tePoint = prev.get((foodPosition[0], foodPosition[1]))
            path = path[::-1]
            # print(path)
            # list_po = copy.deepcopy(snake.postition_list())
            for k in path:
                if len(k) != 2:
                    snake.handle(k[2])
                    snake.move()
            # snake.draw_fake(surface)
            # snake.draw_head(surface)
            # food.draw(surface)
            # screen.blit(surface, (0, 0))
            # pygame.display.update()
            # clock.tick(1)    
            
            if snake.get_head_position() == food.position:
                print(22)
                prev3={}
                if bfs_check(snake.get_ass_position(),snake,surface,prev3) == True and len(prev3) > 1:
                    check = False
                    snake.reload_positions(list_po)        
                    snake.direction = copy.deepcopy(dir_begin)   
                # if check == True:
                    print(2)
                    for i in path:
                        drawGrid(surface)
                        for j in path:
                            r = pygame.Rect((j[0], j[1]), (GRIDSIZE, GRIDSIZE))
                            pygame.draw.rect(surface, BFSPath, r)
                        if len(i) != 2:
                            snake.handle(i[2])
                            snake.move()
                        if snake.get_head_position() == food.position:
                            snake.length += 1
                            score += 1
                            food.randomize_position()
                            food.check_position(snake)
                        snake.draw(surface)
                        snake.draw_head(surface)
                        snake.draw_ass(surface)
                        food.draw(surface)
                        screen.blit(surface, (0, 0))
                        # text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
                        # screen.blit(text, (5, 10))
                        pygame.display.update()
                        clock.tick(FPS)
                else: 
                    check = True
        
        if check == True or answer == False:
            snake.reload_positions(list_po)      
            snake.direction = copy.deepcopy(dir_begin)       
            print(1)
            
            prev2 = {}
            if bfs_check(snake.get_ass_position(),snake,surface,prev2) == True and len(prev2) >= 1:
                print(3)
                snake.reload_positions(list_po)
                foodPosition = copy.deepcopy(snake.get_ass_position())
                tePoint = copy.deepcopy(prev2.get(foodPosition))
                snakeHead = (int(snake.get_head_position()[0]), int(snake.get_head_position()[1]))
                path = []
                while foodPosition != snakeHead:
                    path.append(foodPosition)
                    foodPosition = tePoint
                    if foodPosition is None:
                        break
                    print(foodPosition)
                    tePoint = prev2.get((foodPosition[0], foodPosition[1]))
                path = path[::-1]
                for i in path:
                    drawGrid(surface)
                    # for j in path:
                    #     r = pygame.Rect((j[0], j[1]), (GRIDSIZE, GRIDSIZE))
                    #     pygame.draw.rect(surface, BFSPath, r)
                    if len(i) != 2:
                        snake.handle(i[2])
                        snake.move()
                    if snake.get_head_position() == food.position:
                        snake.length += 1
                        score += 1
                        food.randomize_position()
                        food.check_position(snake)
                    snake.draw(surface)
                    snake.draw_head(surface)
                    snake.draw_ass(surface)
                    food.draw(surface)
                    screen.blit(surface, (0, 0))
                    pygame.display.update()
                    clock.tick(FPS)
                    
                if len(path)==0:
                    print(5)
                    list_po = copy.deepcopy(snake.postition_list())
                    dir_begin = copy.deepcopy(snake.direction)
                    prev6 ={}
                    drawGrid(surface)
                    if snake.any_possible_move() ==  True:
                        snake.move()
                        if bfs_check(snake.get_ass_position(),snake,surface,prev6) == True and len(prev6) > 1:
                            snake.draw(surface)
                            snake.draw_head(surface)
                            snake.draw_ass(surface)
                            food.draw(surface)
                            screen.blit(surface, (0, 0))
                            pygame.display.update()
                            clock.tick(FPS)
                        else:
                            snake.reload_positions(list_po)      
                            snake.direction = copy.deepcopy(dir_begin)
                    # continue
            else:
                print(5)
                list_po = copy.deepcopy(snake.postition_list())
                dir_begin = copy.deepcopy(snake.direction)
                prev6 ={}
                drawGrid(surface)
                if snake.any_possible_move() ==  True:
                    snake.move()
                    if bfs_check(snake.get_ass_position(),snake,surface,prev6) == True and len(prev6) > 1:
                        snake.draw(surface)
                        snake.draw_head(surface)
                        snake.draw_ass(surface)
                        food.draw(surface)
                        screen.blit(surface, (0, 0))
                        pygame.display.update()
                        clock.tick(FPS)
                    else:
                        snake.reload_positions(list_po)      
                        snake.direction = copy.deepcopy(dir_begin)
                # continue

if __name__ == '__main__':
    main()
