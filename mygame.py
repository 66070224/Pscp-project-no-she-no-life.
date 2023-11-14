import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900

pygame.display.set_caption("Mygame")
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
frame = pygame.time.Clock()


def draw_start_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        SCREEN.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('My Game', True, (255, 255, 255))
        start_button = font.render('Start(space)', True, (255, 255, 255))
        SCREEN.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))
        SCREEN.blit(start_button, (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT/2 + start_button.get_height()/2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return "game"
        pygame.display.update()

def draw_game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        SCREEN.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('Q - Quit', True, (255, 255, 255))
        SCREEN.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/3))
        SCREEN.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
        SCREEN.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return "menu"
        if keys[pygame.K_q]:
            pygame.quit()
            quit()
        pygame.display.update()

def maingame():
    bg_image = pygame.image.load("img/grass_51.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_x, bg_y = 0, 0

    text_font = pygame.font.SysFont("monospace", 50)

    monster_cooldown = 0
    bullet_cooldown = 0
    cooldown = 3500
    monster_reducecooldown = 10000

    class Player:
        def __init__(self):
            self.walkRight = [pygame.image.load('img/player/R1.png'), pygame.image.load('img/player/R2.png'), pygame.image.load('img/player/R3.png'), pygame.image.load('img/player/R4.png'), pygame.image.load('img/player/R5.png'), pygame.image.load('img/player/R6.png'), pygame.image.load('img/player/R7.png'), pygame.image.load('img/player/R8.png'), pygame.image.load('img/player/R9.png')]
            self.walkLeft = [pygame.image.load('img/player/L1.png'), pygame.image.load('img/player/L2.png'), pygame.image.load('img/player/L3.png'), pygame.image.load('img/player/L4.png'), pygame.image.load('img/player/L5.png'), pygame.image.load('img/player/L6.png'), pygame.image.load('img/player/L7.png'), pygame.image.load('img/player/L8.png'), pygame.image.load('img/player/L9.png')]
            self.walkCount = 0
            self.image = pygame.image.load('img/player/R1.png')
            self.rect = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            self.diraction = 'r'
            self.health = 100
            self.stamina = 200
            self.tired = False
            self.damage = 50
            self.walk = 2
            self.immortal = False
            self.experience = 0
            self.expperlevel = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
            self.level = 0
            self.hit = False
            self.shootcooldown = 250
            self.shootrange = 500

        def update(self, key_input):
            self.walkjing = False
            self.dx = 0
            self.dy = 0
            if key_input[pygame.K_LSHIFT] and self.stamina >= 0 and not self.tired:
                step = self.walk + 2
                self.stamina -= 0.5
            else:
                step = self.walk
                if self.stamina < 200:
                    if self.stamina < 50:
                        self.tired = True
                    else:
                        self.tired = False
                    self.stamina += 0.25
            if key_input[pygame.K_a]:
                self.diraction = 'l'
                self.dx -= step
                self.walkjing = True
            if key_input[pygame.K_w]:
                self.dy -= step
                self.walkjing = True
            if key_input[pygame.K_d]:
                self.diraction = 'r'
                self.dx += step
                self.walkjing = True
            if key_input[pygame.K_s]:
                self.dy += step
                self.walkjing = True

            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if self.walkjing:
                if self.diraction == 'l':
                    self.image = self.walkLeft[self.walkCount//3]
                    self.walkCount += 1
                elif self.diraction == 'r':
                    self.image = self.walkRight[self.walkCount//3]
                    self.walkCount += 1
            else:
                if self.diraction == 'l':
                    self.image = self.walkLeft[0]
                elif self.diraction == 'r':
                    self.image = self.walkRight[0]
                self.walkCount = 0
            self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            if self.hit:
                self.hit = False
                self.immortal = True
                self.health -= monster.damage
                self.immortal_time = pygame.time.get_ticks() + 1000
            if self.immortal and pygame.time.get_ticks() >= self.immortal_time:
                self.immortal = False
                self.immortal_time = 0

            if self.experience >= self.expperlevel[self.level] and self.level < 10:
                if self.level != 0:
                    self.experience -= self.expperlevel[self.level]
                self.level += 1
                self.health = 100
                self.damage += 10
                self.shootcooldown -= 25
                self.shootrange += 50

            if self.stamina > 0:
                self.stamina_image = pygame.Surface((self.stamina/4, 5))
                self.stamina_image.fill('Blue')
                self.stamina_rect = self.stamina_image.get_rect(center=(SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)-30))
            if self.health > 0:
                self.health_image = pygame.Surface((self.health/2, 5))
                self.health_image.fill('Red')
                self.health_rect = self.health_image.get_rect(center=(SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)-25))
        
        def draw(self):
            if self.diraction == 'l':
                SCREEN.blit(self.image, self.rect)
                self.walkCount += 1
            elif self.diraction == 'r':
                SCREEN.blit(self.image, self.rect)
                self.walkCount += 1
            if self.stamina > 0:
                SCREEN.blit(self.stamina_image, self.stamina_rect)
            if self.health > 0:
                SCREEN.blit(self.health_image, self.health_rect)


    class Monster(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.right = [pygame.image.load('img/goblin/R1E.png'), pygame.image.load('img/goblin/R2E.png'), pygame.image.load('img/goblin/R3E.png'), pygame.image.load('img/goblin/R4E.png'), pygame.image.load('img/goblin/R5E.png'), pygame.image.load('img/goblin/R6E.png'), pygame.image.load('img/goblin/R7E.png'), pygame.image.load('img/goblin/R8E.png'), pygame.image.load('img/goblin/R9E.png'), pygame.image.load('img/goblin/R10E.png'), pygame.image.load('img/goblin/R11E.png')]
            self.left = [pygame.image.load('img/goblin/L1E.png'), pygame.image.load('img/goblin/L2E.png'), pygame.image.load('img/goblin/L3E.png'), pygame.image.load('img/goblin/L4E.png'), pygame.image.load('img/goblin/L5E.png'), pygame.image.load('img/goblin/L6E.png'), pygame.image.load('img/goblin/L7E.png'), pygame.image.load('img/goblin/L8E.png'), pygame.image.load('img/goblin/L9E.png'), pygame.image.load('img/goblin/L10E.png'), pygame.image.load('img/goblin/L11E.png')]
            self.image = pygame.image.load('img/goblin/R1E.png')
            self.walkCount = 0
            self.diraction = 'r'
            spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
            if spawn_side == 'top':
                spawn_x = random.randint(0, SCREEN_WIDTH)
                spawn_y = -50
            elif spawn_side == 'bottom':
                spawn_x = random.randint(0, SCREEN_WIDTH)
                spawn_y = SCREEN_HEIGHT + 50
            elif spawn_side == 'left':
                spawn_x = -50
                spawn_y = random.randint(0, SCREEN_HEIGHT)
            elif spawn_side == 'right':
                spawn_x = SCREEN_WIDTH + 50
                spawn_y = random.randint(0, SCREEN_HEIGHT)
            self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
            self.health = 100
            self.damage = 25
            self.walk = 1
        
        def update(self):
            dx = SCREEN_WIDTH//2 - self.rect.centerx
            dy = SCREEN_HEIGHT//2 - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                self.dx = (dx / distance) * self.walk
                self.dy = (dy / distance) * self.walk
            self.rect.x += self.dx - player.dx
            self.rect.y += self.dy - player.dy

            self.walkjing = False
            if self.dx > 0:
                self.diraction = 'r'
                self.walkjing = True
            elif self.dx < 0:
                self.diraction = 'l'
                self.walkjing = True
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.diraction == 'l' and self.walkjing:
                self.image = self.left[self.walkCount//3]
                self.walkCount += 1
            elif self.diraction == 'r' and self.walkjing:
                self.image = self.right[self.walkCount//3]
                self.walkCount += 1

            if self.health <= 0:
                self.kill()
                exp = Exp(self.rect.x, self.rect.y)
                exps.add(exp)
                return
            if self.rect.colliderect(player.rect) and not player.immortal:
                player.hit = True

        def draw(self):
            SCREEN.blit(self.image, self.rect)


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, mouse_pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            self.image.fill("Yellow")
            self.rect = self.image.get_rect(center=(player.rect.x+30, player.rect.y+35))
            self.damage = 50
            self.speed = 10
            self.derespawn = pygame.time.get_ticks() + player.shootrange

            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            distance = max(1, math.sqrt(dx ** 2 + dy ** 2))
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed

        def update(self):
            if pygame.time.get_ticks() >= self.derespawn:
                self.kill()
                return
            else:
                hit_monsters = pygame.sprite.spritecollide(self, monsters, False)
                for monster in hit_monsters:
                    monster.health -= self.damage
                    self.kill()
            
            self.rect.x += self.dx - player.dx
            self.rect.y += self.dy - player.dy
        
        def draw(self):
            SCREEN.blit(self.image, self.rect)


    class Exp(pygame.sprite.Sprite):
        def __init__(self,x ,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            self.image.fill("Pink")
            self.rect = self.image.get_rect(center=(x+30, y+35))
            self.exp = 10
        
        def update(self):
            if self.rect.colliderect(player.rect):
                player.experience += self.exp
                self.kill()
            self.rect.x -= player.dx
            self.rect.y -= player.dy
        
        def draw(self):
            SCREEN.blit(self.image, self.rect)

    player = Player()

    monster = Monster()
    monsters = pygame.sprite.Group()

    bullets = pygame.sprite.Group()

    exps = pygame.sprite.Group()

    shooting = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shooting = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                shooting = False
        key_input = pygame.key.get_pressed()
        player.update(key_input)
        if player.health <= 0:
            return "game_over"
        bullets.update()
        monsters.update()
        exps.update()
        bg_x -= player.dx
        bg_y -= player.dy
        bg_x %= bg_image.get_width()
        bg_y %= bg_image.get_height()
        SCREEN.blit(bg_image, (bg_x, bg_y))
        SCREEN.blit(bg_image, (bg_x - bg_image.get_width(), bg_y))
        SCREEN.blit(bg_image, (bg_x + bg_image.get_width(), bg_y))
        SCREEN.blit(bg_image, (bg_x, bg_y - bg_image.get_height()))
        SCREEN.blit(bg_image, (bg_x, bg_y + bg_image.get_height()))
        SCREEN.blit(bg_image, (bg_x - bg_image.get_width(), bg_y - bg_image.get_height()))
        SCREEN.blit(bg_image, (bg_x + bg_image.get_width(), bg_y - bg_image.get_height()))
        SCREEN.blit(bg_image, (bg_x - bg_image.get_width(), bg_y + bg_image.get_height()))
        SCREEN.blit(bg_image, (bg_x + bg_image.get_width(), bg_y + bg_image.get_height()))

        if shooting and pygame.time.get_ticks() >= bullet_cooldown:
            bullet_cooldown = pygame.time.get_ticks() + player.shootcooldown
            mouse_pos = pygame.mouse.get_pos()
            bullet = Bullet(mouse_pos)
            bullets.add(bullet)

        if pygame.time.get_ticks() >= monster_cooldown:
            monster_cooldown = pygame.time.get_ticks() + cooldown
            monster = Monster()
            monsters.add(monster)
        
        if pygame.time.get_ticks() >= monster_reducecooldown and monster_cooldown > 100:
            monster_cooldown -= 100
            monster_reducecooldown = pygame.time.get_ticks() + 10000

        SCREEN.blit(bg_image, (bg_x, bg_y))
        player.draw()
        bullets.draw(SCREEN)
        monsters.draw(SCREEN)
        exps.draw(SCREEN)
        textlevel = text_font.render(str(player.level), 1, (0, 0, 0))
        SCREEN.blit(textlevel, (0, 0))

        pygame.display.update()
        frame.tick(60)

now = 'menu'
while True:
    if now == "menu":
        now = draw_start_menu()
    if now == "game":
        now = maingame()
    if now == 'game_over':
        now = draw_game_over_screen()
