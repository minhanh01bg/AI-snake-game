import pygame
import sys
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20 # kick thuoc moi o
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
YELLOW = (255,255,0)
RED = (255,0,0)
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT =(1,0)

clock = pygame.time.Clock()
def drawGrid(surface):
    for y in range(0,int(GRID_HEIGHT)):
        for x in range(0,int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions=[((SCREEN_WIDTH)/2,(SCREEN_HEIGHT)/2)]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
        self.color = (17,24,47)

    def get_head_position(self):
        return self.positions[0]

    def turn(self,point): # direction
        if self.length > 1 and (point[0] * -1,point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]: # đầu con rắn bị trùng với thân của nó
            self.reset()
        else:
            self.positions.insert(0,new) # insert vào top 
            if len(self.positions) > self.length: # thêm vào đầu bớt ở cuối
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions=[((SCREEN_WIDTH)/2,(SCREEN_HEIGHT)/2)]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])

    def draw(self,surface):#draw snake thân
        for p in self.positions:
            r = pygame.Rect((p[0],p[1]),(GRIDSIZE,GRIDSIZE))
            pygame.draw.rect(surface,RED,r)
            # pygame.draw.rect(surface,RED,r,1)#border

    def handle_keys(self):#di chuyen
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
                    
    def handle(self,dir):
        if dir =='u':
            self.turn(UP)
        elif dir=='d':
            self.turn(DOWN)
        elif dir == 'l':
            self.turn(LEFT)
        elif dir == 'r':
            self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (233,163,49)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0,GRID_WIDTH-1)*GRIDSIZE,random.randint(0,GRID_HEIGHT-1)*GRIDSIZE)

    def draw(self,surface):
        r = pygame.Rect((self.position[0],self.position[1]),(GRIDSIZE,GRIDSIZE))
        pygame.draw.rect(surface,self.color,r)
        pygame.draw.rect(surface,(93, 216, 228), r,1)#border

# class point:
#     def __init__(self,a,b):
#         self.a = a
#         self.b = b

  
  
        
def bfs(food,snake,surface):
    queue = []
    queue.append(snake.get_head_position())
    found = False
    list = []
    # inqueue.append(point(0,0,0))
    # for y in range(0,int(GRID_HEIGHT)):
    #     for x in range(0,int(GRID_WIDTH)):
    #         poi = [int(x*GRIDSIZE),int(y*GRIDSIZE),0]
    #         list.append(poi)
        # print()
    
    # list.remove([400,460])
    # if [400, 460,0] in list:
        # print(True)
        
    # for y in range(0,int(GRID_HEIGHT*GRID_WIDTH)):
            # print(list[y])
    # print(snake.get_head_position())
    list.append(snake.get_head_position())
    prev = []
    while len(queue) !=0:
        idx = queue.pop(0)
        cur = idx
        x = UP[0]
        y = UP[1]
        new = (((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT)
        if new == food.position:
            found = True
            return True
        if  new not in snake.positions[2:] and new not in list: 
            queue.append(new)
            list.append(new)
            r = pygame.Rect((((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT),(GRIDSIZE,GRIDSIZE))
            pygame.draw.rect(surface,YELLOW,r)
        x = DOWN[0]
        y = DOWN[1]
        new = (((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT)
        if new == food.position:
            found = True
            return True
        if  new not in snake.positions[2:] and new not in list: 
            queue.append(new)
            list.append(new)
            r = pygame.Rect((((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT),(GRIDSIZE,GRIDSIZE))
            pygame.draw.rect(surface,YELLOW,r)
        x = LEFT[0]
        y = LEFT[1]
        new = (((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT)
        if new == food.position:
            found = True
            return True
        if  new not in snake.positions[2:] and new not in list: 
            queue.append(new)
            list.append(new)
            r = pygame.Rect((((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT),(GRIDSIZE,GRIDSIZE))
            pygame.draw.rect(surface,YELLOW,r)
            
        x = RIGHT[0]
        y = RIGHT[1]
        new = (((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT)
        if new == food.position:
            found = True
            return True
        if  new not in snake.positions[2:] and new not in list: 
            queue.append(new)
            list.append(new)
            r = pygame.Rect((((cur[0] + (x*GRIDSIZE))%SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE))%SCREEN_HEIGHT),(GRIDSIZE,GRIDSIZE))
            pygame.draw.rect(surface,YELLOW,r)
    return found


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    drawGrid(surface)
    snake = Snake()
    food = Food()
    FPS = 10
    myfont = pygame.font.SysFont('monospace',16)
    score = 0
    while True:
        snake.handle_keys()
        drawGrid(surface)
        print(bfs(food,snake,surface))
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface) 
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(score), 1, (0,0,0))
        screen.blit(text, (5, 10))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()