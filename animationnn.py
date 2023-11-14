import pygame
import math
import random

pygame.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Vampire Survivors")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
standright = pygame.image.load('R1.png')
standleft = pygame.image.load('L1.png')
clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 4
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.direction = "d"
        self.health = 100
    
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif man.up and self.direction == "a":
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.up and self.direction == "d":
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.down and self.direction == "d":
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.direction == "a":
            win.blit(standleft, (self.x, self.y))
        elif self.direction == "d":
            win.blit(standright, (self.x, self.y))
    
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    collision_gap = 10

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.speed = 2
        self.direction = "right"

    def draw(self, win, player):
        self.move(player)
        if self.direction == "right":
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
        
        self.walkCount += 1
        if self.walkCount >= 33:
            self.walkCount = 0
    
    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx /= distance
            dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed

        if dx >= 0:
            self.direction = "right"
        else:
            self.direction = "left"
    
    def handle_collision(cls, goblin1, goblin2):
        dx = goblin1.x - goblin2.x
        dy = goblin1.y - goblin2.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            dx /= distance
            dy /= distance

        move_distance = cls.collision_gap / 2.0

        goblin1.x += dx * move_distance
        goblin1.y += dy * move_distance
        goblin2.x -= dx * move_distance
        goblin2.y -= dy * move_distance


def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    for goblin in goblins:
        goblin.draw(win, man)

    pygame.display.update()

#mainloop
man = player(600, 350, 64, 64)
goblins = []

num_goblins = random.randint(5, 10)

for _ in range(num_goblins):
    goblin_x = random.randint(100, 1180)
    goblin_y = random.randint(100, 620)
    goblin = enemy(goblin_x, goblin_y, 64, 64)
    goblins.append(goblin)

run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and keys[pygame.K_a]:
        man.x -= man.speed
        man.y -= man.speed
        man.left = True
        man.right = False
        man.direction = "a"
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        man.x += man.speed
        man.y -= man.speed
        man.right = True
        man.left = False
        man.direction = "d"
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        man.x -= man.speed
        man.y += man.speed
        man.left = True
        man.right = False
        man.direction = "a"
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        man.x += man.speed
        man.y += man.speed
        man.right = True
        man.left = False
        man.direction = "d"
    elif keys[pygame.K_a]:
        man.x -= man.speed
        man.left = True
        man.right = False
        man.direction = "a"
    elif keys[pygame.K_d]:
        man.x += man.speed
        man.right = True
        man.left = False
        man.direction = "d"
    elif keys[pygame.K_w]:
        man.y -= man.speed
        man.up = True
    elif keys[pygame.K_s]:
        man.y += man.speed
        man.down = True
    else:
        man.right = False
        man.left = False
        man.walkCount = 0

    player_rect = pygame.Rect(man.x, man.y, man.width, man.height)
    for goblin in goblins:
        goblin_rect = pygame.Rect(goblin.x, goblin.y, goblin.width, goblin.height)
        if player_rect.colliderect(goblin_rect):
            man.health -= 5
            
    redrawGameWindow()

pygame.quit()
