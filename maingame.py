import pygame
import random
import math

pygame.init()

WIDTH = 1800
HEIGHT = 900

pygame.display.set_caption("Mygame")
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
frame = pygame.time.Clock()

def maingame():
    bg_image = pygame.image.load("img/grass_51.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    bg_x, bg_y = 0, 0

    text_font = pygame.font.SysFont("monospace", 50)

    monster_cooldown = 0
    bullet_cooldown = 0
    cooldown = 5000

    class Player:
        def __init__(self):
            self.image = pygame.Surface((20, 20))
            self.image.fill("Green")
            self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.direction = 'w'
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

        def update(self, key_input):
            keya, keyw, keyd, keys, now = False, False, False, False, 0
            self.dx = 0
            self.dy = 0
            if key_input[pygame.K_a]:
                keya = True
                now += 1
            if key_input[pygame.K_w]:
                keyw = True
                now += 1
            if key_input[pygame.K_d]:
                keyd = True
                now += 1
            if key_input[pygame.K_s]:
                keys = True
                now += 1
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
            if now > 0:
                self.direction = ''
            if keya:
                self.dx -= step
                self.direction += 'a'
            if keyw:
                self.dy -= step
                self.direction += 'w'
            if keyd:
                self.dx += step
                self.direction += 'd'
            if keys:
                self.dy += step
                self.direction += 's'
            
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

            if self.stamina > 0:
                self.stamina_image = pygame.Surface((self.stamina/4, 5))
                self.stamina_image.fill('Blue')
                self.stamina_rect = self.stamina_image.get_rect(center=(self.rect.x+10, self.rect.y-10))
            if self.health > 0:
                self.health_image = pygame.Surface((self.health/2, 5))
                self.health_image.fill('Red')
                self.health_rect = self.health_image.get_rect(center=(self.rect.x+10, self.rect.y-5))
        
        def draw(self):
            SCREEN.blit(self.image, self.rect)
            if self.stamina > 0:
                SCREEN.blit(self.stamina_image, self.stamina_rect)
            if self.health > 0:
                SCREEN.blit(self.health_image, self.health_rect)


    class Monster(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((20, 20))
            self.image.fill("Red")
            spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
            if spawn_side == 'top':
                spawn_x = random.randint(0, WIDTH)
                spawn_y = -50
            elif spawn_side == 'bottom':
                spawn_x = random.randint(0, WIDTH)
                spawn_y = HEIGHT + 50
            elif spawn_side == 'left':
                spawn_x = -50
                spawn_y = random.randint(0, HEIGHT)
            elif spawn_side == 'right':
                spawn_x = WIDTH + 50
                spawn_y = random.randint(0, HEIGHT)
            self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
            self.health = 100
            self.damage = 25
            self.walk = 1
        
        def update(self):
            if self.health <= 0:
                self.kill()
                exp = Exp(self.rect.x, self.rect.y)
                exps.add(exp)
                return
            if self.rect.colliderect(player.rect) and not player.immortal:
                player.hit = True

            dx = WIDTH//2 - self.rect.centerx
            dy = HEIGHT//2 - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                self.dx = (dx / distance) * self.walk
                self.dy = (dy / distance) * self.walk
            self.rect.x += self.dx - player.dx
            self.rect.y += self.dy - player.dy

        def draw(self):
            SCREEN.blit(self.image, self.rect)


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, diraction):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            self.image.fill("Yellow")
            self.rect = self.image.get_rect(center=(player.rect.x+10, player.rect.y+10))
            self.direction = diraction
            self.speed = 20
            self.damage = 50
            self.time = 0
            self.derespawn = pygame.time.get_ticks()+500
        
        def update(self):
            dx = 0
            dy = 0
            if pygame.time.get_ticks() >= self.derespawn:
                self.kill()
                return
            else:
                hit_monsters = pygame.sprite.spritecollide(self, monsters, False)
                for monster in hit_monsters:
                    monster.health -= self.damage
                    self.kill()
            if 'a' in self.direction:
                dx -= self.speed
            if 'w' in self.direction:
                dy -= self.speed
            if 'd' in self.direction:
                dx += self.speed
            if 's' in self.direction:
                dy += self.speed
            
            self.rect.x += dx - player.dx
            self.rect.y += dy - player.dy

        def draw(self):
            SCREEN.blit(self.image, self.rect)


    class Exp(pygame.sprite.Sprite):
        def __init__(self,x ,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            self.image.fill("Green")
            self.rect = self.image.get_rect(center=(x+10, y+10))
            self.exp = 20
        
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

    bullet = Bullet(player.direction)
    bullets = pygame.sprite.Group()

    exp = Exp(monster.rect.x, monster.rect.y)
    exps = pygame.sprite.Group()


    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
        key_input = pygame.key.get_pressed()
        player.update(key_input)
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
        if key_input[pygame.K_SPACE] and pygame.time.get_ticks() >= bullet_cooldown:
            bullet_cooldown = pygame.time.get_ticks() + 250
            bullet = Bullet(player.direction)
            bullets.add(bullet)
        if pygame.time.get_ticks() >= monster_cooldown:
            monster_cooldown = pygame.time.get_ticks() + cooldown
            if cooldown > 20:
                cooldown -= 1
            monster = Monster()
            monsters.add(monster)
        SCREEN.blit(bg_image, (bg_x, bg_y))
        player.draw()
        bullets.draw(SCREEN)
        monsters.draw(SCREEN)
        exps.draw(SCREEN)
        textlevel = text_font.render(str(player.level), 1, (0, 0, 0))
        SCREEN.blit(textlevel, (0, 0))

        pygame.display.update()
        frame.tick(60)

def mainmenu():
    start_buttom_img = pygame.image.load("img/play_button.png").convert_alpha()


    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            SCREEN.blit(self.image, (self.rect.x, self.rect.y))


    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
        start_buttom = Button(100, 200, start_buttom_img)
        
mainmenu()
