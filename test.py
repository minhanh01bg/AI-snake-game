import pygame
import sys
import random
import copy
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

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
# FONT = pygame.font.SysFont("Arial",20)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            # if (x + y) % 2 == 0:
            r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, (54, 54, 54), r)
            pygame.draw.rect(surface, (169, 201, 153), r,3)
            pygame.draw.rect(surface, (54, 54, 54), r,1)
                
            # else:
                # rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE),
                #                  (GRIDSIZE, GRIDSIZE))
                # pygame.draw.rect(surface, (169, 201, 153), rr)
                # pygame.draw.rect(surface, (54, 54, 54), rr,2)

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
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        # đầu con rắn bị trùng với thân của nó
        if len(self.positions) > 2 and new in self.positions[2:]:
            # self.reset()
            pass
        else:
            self.positions.insert(0, new)  # insert vào top
            if len(self.positions) > self.length:  # thêm vào đầu bớt ở cuối
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH)/2, (SCREEN_HEIGHT)/2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):  # draw snake thân
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, WHITE, r)
            pygame.draw.rect(surface, RED, r, 1)  # border
            
    def draw_head(self,surface):
        snakeSurface = pygame.Surface((GRIDSIZE, GRIDSIZE))
        pygame.draw.circle(snakeSurface,WHITE, (4, 6), 2)
        pygame.draw.circle(snakeSurface, WHITE, (16, 6), 2)
        surface.blit(snakeSurface,self.positions[0])
        
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
    
    def reload_positions(self,positions_load):
        self.positions = copy.deepcopy(positions_load)

    def postition_list(self):
        return self.positions

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
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1:tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
        x = DOWN[0]
        y = DOWN[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
        x = LEFT[0]
        y = LEFT[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
        x = RIGHT[0]
        y = RIGHT[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
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
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1:tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
        x = DOWN[0]
        y = DOWN[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
        x = LEFT[0]
        y = LEFT[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
        x = RIGHT[0]
        y = RIGHT[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[0:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            queue.append(new)
            list.append(new)
            r = pygame.Rect(new, (GRIDSIZE, GRIDSIZE))
            # pygame.draw.rect(surface, BFSPath, r)
    return found

def dfs(food, snake, surface, prev):
    queue = []
    queue.append(snake.get_head_position())
    found = False
    list = []
    list.append(snake.get_head_position())
    while len(queue) != 0:
        idx = queue.pop(0)
        cur = idx
        list.append(idx)
        x = UP[0]
        y = UP[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[2:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'u')
            prev.update({tePoint1:tePoint2})
            queue.insert(0,new)
            # list.append(new)
            
        x = DOWN[0]
        y = DOWN[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[2:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'd')
            prev.update({tePoint1: tePoint2})
            queue.insert(0,new)
            # list.append(new)
            
        x = LEFT[0]
        y = LEFT[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            found = True
            return True
        if new not in snake.positions[2:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'l')
            prev.update({tePoint1: tePoint2})
            # list.append(new)
            queue.insert(0,new)
            
        x = RIGHT[0]
        y = RIGHT[1]
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        if new == food.position:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            found = True
            return True

        if new not in snake.positions[2:] and new not in list:
            tePoint1 = (int(new[0]), int(new[1]))
            tePoint2 = (int(cur[0]), int(cur[1]), 'r')
            prev.update({tePoint1: tePoint2})
            # list.append(new)
            queue.insert(0,new)
            
    return found


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    # drawGrid(surface)
    snake = Snake()
    food = Food()
    FPS =30
    myfont = pygame.font.SysFont('monospace', 16)
    score = 1
    snake_check = copy.deepcopy(snake.postition_list())
    while True:
        # snake.handle_keys()
        prev = {}
        print(bfs(food, snake, surface, prev))
        snakeHead = (int(snake.get_head_position()[0]), int(snake.get_head_position()[1]))
        foodPosition = (int(food.position[0]), int(food.position[1]))
        tePoint = prev.get(foodPosition)
        path = []
        while foodPosition != snakeHead:
            path.append(foodPosition)
            foodPosition = tePoint
            if foodPosition is None:
                break
            print(foodPosition)
            tePoint = prev.get((foodPosition[0], foodPosition[1]))
        path = path[::-1]
        # print(path)
        survay = False
        # print(snake.positions)
        for i in path:
            if len(i) != 2:
                snake.handle(i[2])
                snake.move()
            prev2 = {}
            if snake.get_head_position() == food.position:
                if bfs_check(snake.get_ass_position(),snake,surface,prev2) == True:
                    print(snake.get_ass_position())
                    survay = True
        # print(snake.positions)
        snake.reload_positions(snake_check)
        if survay == True:
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
                food.draw(surface)
                screen.blit(surface, (0, 0))
                text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
                screen.blit(text, (5, 10))
                pygame.display.update()
                clock.tick(FPS)
            snake_check = copy.deepcopy(snake.postition_list())
            
if __name__ == '__main__':
    main()
