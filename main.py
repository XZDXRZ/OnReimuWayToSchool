# FBI Warning:
# Till 2021/08/31, only God and me could understand this code.
# I guess a few months later, only God could understand it.

# 东方上学传
# 共5面
# 讲述灵梦的上学故事
# 自机：博丽灵梦
# 敌机：魔理沙——同居
#      琪露诺——妹妹（？）
#      咲夜——女仆
#      紫妈sdakjfsaijfi——你妈
#      早苗——老师（不干了）

import pygame
import sys, random, time, math

size = (1000,650)
bg_color = (255,255,255)
tick = 10

# Game constant number
PLAYERBULLETDELAY = 7
MARISA_BLOOD = 40
CIRNO_BLOOD = 80
SAKUYA_BLOOD = 60
YAKUMO_BLOOD = 200

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg_color)
pygame.display.set_caption("东方上学传")

player_bullets_delay = 0
player_pos = [0, 0]
grade = 1
communication = [False, False, False, False] #代表8次剧情其中4个
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
        global gg
        if pygame.sprite.spritecollide(player, marisa_bullets, False, pygame.sprite.collide_mask):
            gg = True
        if pygame.sprite.spritecollide(player, cirno_bullets, False, pygame.sprite.collide_mask):
            gg = True
        if pygame.sprite.spritecollide(player, sakuya_bullets, False, pygame.sprite.collide_mask):
            gg = True
        if pygame.sprite.spritecollide(player, yakumo_bullets, False, pygame.sprite.collide_mask):
            gg = True

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
        self.blood = MARISA_BLOOD
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
        self.blood = CIRNO_BLOOD
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
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            x = x if x!=0 else x+1
            y = y if y!=0 else y+1
            self.t = [x*3, y*3]
            self.changed = True

class Sakuya(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/Sakuya_up.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0]/2 - (self.rect.right - self.rect.left)/2, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.character = pygame.image.load('./img/characters/Sakuya.png')
        self.blood = SAKUYA_BLOOD
        self.bullet_num = 0
        self.shoot_CD = 0

    def behit(self):
        if pygame.sprite.spritecollide(sakuya, player_bullets, True, pygame.sprite.collide_mask):
            self.blood -= 1

    def shoot(self):
        global player_pos
        if self.shoot_CD <= 5: #在四个方向生成子弹
            for i in range(7, 22):
                sakuya_bullets.add(Sakuya_Bullets(45, [player_pos[0]-10*i,player_pos[1]-10*i], math.sqrt(((10*i)**2)*2)))
            for i in range(7, 22):
                sakuya_bullets.add(Sakuya_Bullets(135, [player_pos[0]-10*i,player_pos[1]+10*i], math.sqrt(((10*i)**2)*2)))
            for i in range(7, 22):
                sakuya_bullets.add(Sakuya_Bullets(225, [player_pos[0]+10*i,player_pos[1]+10*i], math.sqrt(((10*i)**2)*2)))
            for i in range(7, 22):
                sakuya_bullets.add(Sakuya_Bullets(315, [player_pos[0]+10*i,player_pos[1]-10*i], math.sqrt(((10*i)**2)*2)))
            self.shoot_CD = 100
        for bullet in sakuya_bullets:
            bullet.move()
        self.shoot_CD -= 1

class Sakuya_Bullets(pygame.sprite.Sprite):
    def __init__(self, direction, pos, distance):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.origin_pos = pos
        self.direction = math.radians(direction)
        self.distance = distance
        self.t = [math.sin(self.direction)*2, math.cos(self.direction)*2]

    def move(self):
        self.rect = self.rect.move(self.t)
        if (self.origin_pos[0]-self.rect.left)**2 + (self.origin_pos[1]-self.rect.top)**2 >= self.distance**2:
            self.kill()

class Yakumo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/Yakumo_up.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (size[0]/2 - (self.rect.right - self.rect.left)/2, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.character = pygame.image.load('./img/characters/Yakumo.png')
        self.blood = YAKUMO_BLOOD
        self.t = 0
        self.shoot_CD = 0

    # def func(self, x):
    #     return -(2/9)*x+14/3

    def func(self, x):
        return -(1.0/19)*x+14/3

    def behit(self):
        if pygame.sprite.spritecollide(sakuya, player_bullets, True, pygame.sprite.collide_mask):
            self.blood -= 1

    def shoot(self):
        if self.shoot_CD >= 2:
            yakumo_bullets.add(Yakumo_Bullets(self.t*self.func(self.t)))
            yakumo_bullets.add(Yakumo_Bullets(self.t*self.func(self.t)+90))
            yakumo_bullets.add(Yakumo_Bullets(self.t*self.func(self.t)+180))
            yakumo_bullets.add(Yakumo_Bullets(self.t*self.func(self.t)+270))
            self.shoot_CD = 0
        self.t += 0.7
        for bullet in yakumo_bullets:
            bullet.move()
        self.shoot_CD += 1

class Yakumo_Bullets(pygame.sprite.Sprite):
    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./img/gameimg/bullet.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = yakumo.rect.left + (yakumo.rect.right - yakumo.rect.left)/2, yakumo.rect.top + (yakumo.rect.bottom - yakumo.rect.top)/2
        self.direction = math.radians(direction)
        self.t = [math.sin(self.direction), math.cos(self.direction)]

    def move(self):
        factor = 6
        self.rect.left = self.rect.left + self.t[0]*factor
        self.rect.top = self.rect.top + self.t[1]*factor
        # 我草他妈的self.rect.move()

def continue_next():
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
sakuya = Sakuya()
yakumo = Yakumo()
player_bullets = pygame.sprite.Group()
marisa_bullets = pygame.sprite.Group()
cirno_bullets = pygame.sprite.Group()
sakuya_bullets = pygame.sprite.Group()
yakumo_bullets = pygame.sprite.Group()

def animate():
    global player_pos, grade, win
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
            pygame.display.flip()
            text = []
            text.append(font.render("你醒啦", True, (255,255,255)))
            text.append(font.render("什么我已经变成女孩子了吗", True, (255,255,255)))
            text.append(font.render("不我只是想让你借我抄下作业", True, (255,255,255)))
            text.append(font.render("没门", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            continue_next()
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
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(marisa.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            continue_next()
            marisa.kill()
            for bullet in marisa_bullets.sprites():
                bullet.kill()
    if grade == 2: #琪露诺关
        if not communication[1]: #琪露诺先行剧情
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,0,size[0],size[1]))
            pygame.display.flip()
            text = []
            text.append(font.render("陪我玩", True, (255,255,255)))
            text.append(font.render("不行我要去上学", True, (255,255,255)))
            text.append(font.render("陪 我 玩", True, (255,255,255)))
            text.append(font.render("你夏树吗你", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(cirno.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(cirno.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            continue_next()
            communication[1] = True
        screen.blit(cirno.image, cirno.rect)
        cirno.shoot()
        cirno.behit()
        cirno_blood = font.render("琪露诺血量：" + str(cirno.blood), True, (0,0,0))
        screen.blit(cirno_blood, (0,0))
        for bullet in cirno_bullets.sprites():
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.left < 0 or bullet.rect.left > size[0] or bullet.rect.top > size[1]:
                bullet.kill()
        if cirno.change_delay >= 140:
            for bullet in cirno_bullets:
                bullet.stage = 2
        if cirno.blood <= 0:
            grade = 3
            text = []
            text.append(font.render("欺负小女孩可不道德啊！", True, (255,255,255)))
            text.append(font.render("明明是你先打的我好不好", True, (255,255,255)))
            text.append(font.render("不管啦，反正你就是欺负我", True, (255,255,255)))
            text.append(font.render("讲不讲理啊你！", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(cirno.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(cirno.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            continue_next()
            cirno.kill()
            for bullet in cirno_bullets:
                bullet.kill()
        if not cirno.changed:
            cirno.change_delay += 1
    if grade == 3: # 咲夜关
        if not communication[2]:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,0,size[0],size[1]))
            pygame.display.flip()
            text = []
            text.append(font.render("主人你早饭没吃", True, (255,255,255)))
            text.append(font.render("不行要迟到了", True, (255,255,255)))
            text.append(font.render("要迟到也得吃", True, (255,255,255)))
            text.append(font.render("你不去服侍大小姐来这凑热闹干嘛", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(sakuya.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(sakuya.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (100,500))
            pygame.display.flip()
            continue_next()
            communication[2] = True
        screen.blit(sakuya.image, sakuya.rect)
        sakuya.shoot()
        sakuya.behit()
        sakuya_blood = font.render("十六夜□夜血量：" + str(sakuya.blood), True, (0,0,0)) #十六夜咲夜显示有bug
        screen.blit(sakuya_blood, (0,0))
        for bullet in sakuya_bullets.sprites():
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.left < 0 or bullet.rect.left > size[0] or bullet.rect.top > size[1]:
                bullet.kill()
        if sakuya.blood <= 0:
            grade = 4
            text = []
            text.append(font.render("你再打我就不干了", True, (255,255,255)))
            text.append(font.render("我本来就没想让你干啊", True, (255,255,255)))
            text.append(font.render("凎", True, (255,255,255))) # ko ji da yo!
            text.append(font.render("你说啥？", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(sakuya.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(sakuya.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            continue_next()
            sakuya.kill()
            for bullet in sakuya_bullets:
                bullet.kill()
    if grade == 4: #紫妈
        if not communication[3]:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,0,size[0],size[1]))
            pygame.display.flip()
            text = []
            text.append(font.render("听说你刚刚欺负琪露诺了？", True, (255,255,255)))
            text.append(font.render("我不是我没有", True, (255,255,255)))
            text.append(font.render("还狡辩", True, (255,255,255)))
            text.append(font.render("别啊", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(yakumo.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(yakumo.character, hostile_pos)
            screen.blit(text[2], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[3], (300,500))
            pygame.display.flip()
            continue_next()
            communication[3] = True
        screen.blit(yakumo.image, yakumo.rect)
        yakumo.shoot()
        yakumo.behit()
        yakumo_blood = font.render("八云紫血量：" + str(yakumo.blood), True, (0,0,0))
        screen.blit(yakumo_blood, (0,0))
        for bullet in yakumo_bullets.sprites():
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.left < 0 or bullet.rect.left > size[0] or bullet.rect.top > size[1] or bullet.rect.top <= 0:
                bullet.kill()
        if yakumo.blood <= 0:
            win = True
            text = []
            text.append(font.render("反了你", True, (255,255,255)))
            text.append(font.render("你先打的好不好", True, (255,255,255)))
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(yakumo.character, hostile_pos)
            screen.blit(text[0], (500,500))
            pygame.display.flip()
            continue_next()
            pygame.draw.rect(screen, (0,0,0), (0,450,1000,200), 0)
            screen.blit(reimu.character, reimu_pos)
            screen.blit(text[1], (300,500))
            pygame.display.flip()
            continue_next()
    pygame.display.flip()

running = True
gg = False
win = False

while running: 
    animate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(tick)
    if gg == True:
        font = pygame.font.SysFont("Times", 70)
        gameover_text = font.render("Game Over!", True, (255, 100, 100))
        screen.fill((255,0,0))
        screen.blit(gameover_text, (340, 280))
        pygame.display.flip()
        time.sleep(1)
        break
    if win==True:
        font = pygame.font.SysFont("Times", 70)
        win_text = font.render("You Win!", True, (100, 255, 100))
        screen.fill((0,160,0))
        screen.blit(win_text, (340, 280))
        pygame.display.flip()
        time.sleep(1)
        break

pygame.quit()
sys.exit()