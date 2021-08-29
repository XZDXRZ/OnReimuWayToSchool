# FBI Warning:
# Till 2021/06/21, only God and me could understand this code.
# I guess a few months later, only God could understand it.

# 东方上学传
# 共5面
# 讲述灵梦的上学故事
# 自机：博丽灵梦
# 敌机：魔理沙——同居
#      琪露诺——妹妹（？）
#      咲夜——女仆
#      早苗——你妈
#      爱丽丝——老师

from hashlib import blake2b
import pygame
import sys, random, time, math

size = (1000,650)
bg_color = (255,255,255)
tick = 10

# Game constant number
PLAYERBULLETDELAY = 7

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg_color)
pygame.display.set_caption("东方上学传")

player_bullets_delay = 0
player_pos = [0, 0]
grade = 1
communication = [False, False, False, False, False] #代表10次剧情其中5个
hostile_pos = [0, 200]
reimu_pos = [500, 200]
dialog_pos = [0, 500]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/death_point.png')
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (100,50)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.pos = pygame.mouse.get_pos()
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left
        self.pos = list(self.pos)
        self.pos[0] -= self.width/2
        self.pos[1] -= self.height/2
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > size[0]:
            self.pos[0] = size[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > size[1]:
            self.pos[1] = size[1]
        self.rect.left, self.rect.top = self.pos
        return pygame.mouse.get_pos()

    def shoot(self):
        global player_bullets_num, player_bullets_delay
        if player_bullets_delay >= PLAYERBULLETDELAY:
            player_bullets.add(Player_Bullet(self.rect))
            player_bullets_delay = 0
        player_bullets_delay += 1

    def game_over(self):
        global GG
        if pygame.sprite.spritecollide(player, marisa_bullets, False, pygame.sprite.collide_mask):
            GG = True

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pos
        self.out = False

    def move(self):
        self.rect = self.rect.move([0,-10])
        if self.rect.top < 0:
            self.out = True

class Reimu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/Reimu_up.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (100,50)
        self.mask = pygame.mask.from_surface(self.image)
        self.character = pygame.image.load('./img/characters/Reimu.png')

    def move(self):
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left
        self.rect.left, self.rect.top = player.rect.left - self.width/2 + player.width/2, player.rect.top - self.height/2 + player.height/2

class Dock(pygame.sprite.Sprite):
    def __init__(self, bear):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/Dock.png')
        self.rect = self.image.get_rect()
        self.bear = bear
        if self.bear == 'left':
            self.rect.left, self.rect.top = (90, 50)
        else:
            self.rect.left, self.rect.top = (110, 50)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left
        if self.bear == 'left':
            self.rect.left, self.rect.top = player.rect.left - self.width/2 + player.width/2 - 70, player.rect.top - self.height/2 + player.height/2
        else:
            self.rect.left, self.rect.top = player.rect.left - self.width/2 + player.width/2 + 70, player.rect.top - self.height/2 + player.height/2

class Marisa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/marisa_up.png')
        self.image = pygame.transform.scale(self.image, (128, 256))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0]/2 - (self.rect.right - self.rect.left)/2, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot_delay = 0
        self.blood = 1#100
        self.character = pygame.image.load('./img/characters/Marisa.png')
        self.bullet_now = 0
        self.can_shoot = True
        self.big_shoot_delay = 40
        self.bearing = math.atan((self.rect.center[0] - player_pos[0])/(self.rect.center[1] - player_pos[1]))

    def shoot(self): #第一波弹幕
        if self.shoot_delay <= 0 and self.can_shoot:
            marisa_bullets.add(Marisa_Bullets(self.bearing + math.radians(5)))
            marisa_bullets.add(Marisa_Bullets(self.bearing - math.radians(5)))
            marisa_bullets.add(Marisa_Bullets(self.bearing + math.radians(20)))
            marisa_bullets.add(Marisa_Bullets(self.bearing - math.radians(20)))
            marisa_bullets.add(Marisa_Bullets(self.bearing + math.radians(15)))
            marisa_bullets.add(Marisa_Bullets(self.bearing - math.radians(15)))
            marisa_bullets.add(Marisa_Bullets(self.bearing + math.radians(10)))
            marisa_bullets.add(Marisa_Bullets(self.bearing - math.radians(10)))
            self.shoot_delay = 5
            self.bullet_now += 1
        if self.bullet_now >= 5:
            self.can_shoot = False
            self.big_shoot_delay -= 1
        if self.big_shoot_delay <= 0:
            self.can_shoot = True
            self.big_shoot_delay = 40
            self.bullet_now = 0
        for bullet in marisa_bullets.sprites():
            bullet.move()
        self.shoot_delay -= 1

    def behit(self):
        if pygame.sprite.spritecollide(marisa, player_bullets, True, pygame.sprite.collide_mask):
            self.blood -= 1

class Marisa_Bullets(pygame.sprite.Sprite):
    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = marisa.rect.left + (marisa.rect.right - marisa.rect.left)/2, marisa.rect.top + (marisa.rect.bottom - marisa.rect.top)/2
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.t = [math.sin(self.direction)*5.1, math.cos(self.direction)*5.1]

    def move(self):
        self.rect = self.rect.move(self.t)

class Cirno(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/cirno_up.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0]/2 - (self.rect.right - self.rect.left)/2, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.character = pygame.image.load('./img/characters/Cirno.png')
        self.blood = 40
        self.bullet_num = 0
        self.change_delay = 0
        self.changed = False

    def behit(self):
        if pygame.sprite.spritecollide(cirno, player_bullets, True, pygame.sprite.collide_mask):
            self.blood -= 1

    def shoot(self):
        for i in range(30):
            if self.bullet_num <= 100:
                self.bullet_num += 1
                cirno_bullets.add(Cirno_Bullets(random.randint(270, 360), random.randint(40, 500)**2+random.randint(70, 300)**2))
            if self.bullet_num <= 100:
                self.bullet_num += 1
                cirno_bullets.add(Cirno_Bullets(random.randint(0, 90), random.randint(40, 500)**2+random.randint(70, 300)**2))
        for bullet in cirno_bullets:
            bullet.move()

class Cirno_Bullets(pygame.sprite.Sprite):
    def __init__(self, direction, distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = cirno.rect.left + (cirno.rect.right - cirno.rect.left)/2, cirno.rect.top + (cirno.rect.bottom - cirno.rect.top)/2
        self.mask = pygame.mask.from_surface(self.image)
        self.origin_pos = self.rect
        self.direction = math.radians(direction)
        self.distance = distance
        self.t = [math.sin(self.direction)*5.1, math.cos(self.direction)*5.1]
        self.stage = 1
        self.changed = False

    def move(self):
        self.rect = self.rect.move(self.t)
        if (self.origin_pos[0]-self.rect[0])**2+(self.origin_pos[1]-self.rect[1])**2 >= self.distance: # don't need to square
            if self.stage == 1:
                self.t = [0,0]
        if self.stage == 2 and (not self.changed):
            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            # x = x if x==0.0 else x+1
            # y = y if y==0.0 else y+1
            self.t = [x*3, y*3]
            self.changed = True

def Continue():
    next = False
    while not next:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                next = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

player = Player()
reimu = Reimu()
dock_left = Dock(bear = 'left')
dock_right = Dock(bear = 'right')
marisa = Marisa()
cirno = Cirno()
player_bullets = pygame.sprite.Group()
marisa_bullets = pygame.sprite.Group()
cirno_bullets = pygame.sprite.Group()

def animate():
    global player_pos, grade
    player.game_over()
    font = pygame.font.Font('./Font/FZLTHJW.ttf', 30)
    screen.fill(bg_color)
    player_pos = player.move()
    reimu.move()
    dock_left.move()
    dock_right.move()
    player.shoot()
    for player_bullet in player_bullets.sprites():
        player_bullet.move()
        screen.blit(player_bullet.image, player_bullet.rect)
        if player_bullet.out:
            player_bullets.remove(player_bullet)
    screen.blit(reimu.image, reimu.rect)
    screen.blit(dock_left.image, dock_left.rect)
    screen.blit(dock_right.image, dock_right.rect)
    screen.blit(player.image, player.rect)
    if grade == 1: #魔理沙关
        if not communication[0]: #魔理沙先行剧情
            text = []
            text.append(font.render("你醒啦", True, (255,255,255)))
            text.append(font.render("什么我已经变成女孩子了吗", True, (255,255,255)))
            text.append(font.render("不我只是想让你借我抄下作业", True, (255,255,255)))
            text.append(font.render("没门", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            Continue()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            Continue()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            Continue()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            Continue()
            communication[0] = True
        screen.blit(marisa.image, marisa.rect)
        marisa.shoot()
        marisa.behit()
        marisa.bearing = math.atan((marisa.rect.center[0] - player_pos[0])/(marisa.rect.center[1] - player_pos[1]))
        marisa_blood = font.render("魔理沙血量：" + str(marisa.blood), True, (0,0,0))
        screen.blit(marisa_blood, (0,0))
        for bullet in marisa_bullets.sprites():
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.left < 0 or bullet.rect.left > size[0] or bullet.rect.top > size[1]:
                bullet.kill()
        if marisa.blood <= 0: #魔理沙击败剧情
            grade = 2
            text = []
            text.append(font.render("灵梦， 你在干什么啊！灵梦", True, (255,255,255)))
            text.append(font.render("希腊奶", True, (255,255,255)))
            text.append(font.render("凭什么不给我抄作业？你坏！", True, (255,255,255)))
            text.append(font.render("等着挨骂去吧，^_^", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            Continue()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            Continue()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            Continue()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            Continue()
            marisa.kill()
            for bullet in marisa_bullets.sprites():
                bullet.kill()
    if grade == 2: #琪露诺关
        screen.blit(cirno.image, cirno.rect)
        cirno.shoot()
        cirno.behit()
        cirno_blood = font.render("琪露诺血量：" + str(cirno.blood), True, (0,0,0))
        screen.blit(cirno_blood, (0,0))
        for bullet in cirno_bullets.sprites():
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.left < 0 or bullet.rect.left > size[0] or bullet.rect.top > size[1]:
                bullet.kill()
        if cirno.change_delay >= 130:
            for bullet in cirno_bullets:
                bullet.stage = 2
        if cirno.blood <= 0:
            exit()
        if not cirno.changed:
            cirno.change_delay += 1
    pygame.display.flip()

running = True
GG = False

while running:
    animate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(tick)
    if GG == True:
        font = pygame.font.SysFont("Times", 70)
        gameover_text = font.render("Game Over!", True, (255, 100, 100))
        screen.fill((255,0,0))
        screen.blit(gameover_text, (340, 280))
        pygame.display.flip()
        time.sleep(1)
        break