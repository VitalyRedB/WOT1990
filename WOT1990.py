import pygame
from random import randint

pygame.mixer.init()

sound_effect1 = pygame.mixer.Sound('sound_set/TUK.mp3')
sound_effect2 = pygame.mixer.Sound('sounds/shot.wav')
sndEngine = pygame.mixer.Sound('sounds/engine.wav')
sndEngine.set_volume(0.2)
sndMove = pygame.mixer.Sound('sounds/move.wav')
sndMove.set_volume(0.2)
sndStar = pygame.mixer.Sound('sounds/star.wav')
sndLive = pygame.mixer.Sound('sounds/live.wav')


width , height = 800 , 600
FPS = 60
TILE = 32
pygame.init()

font_path = pygame.font.match_font('dejavusans')
fontUA = pygame.font.Font(font_path, 20)
fontUI = pygame.font.Font(None, 30)
fontBig = pygame.font.Font(None, 70)

imgBrick = pygame.image.load('WOT1990_set/images/block_brick.png')
imgTanks = [pygame.image.load(f'WOT1990_set/images/tank{i}.png') for i in range(1,9)]
imgBangs = [pygame.image.load(f'WOT1990_set/images/bang{i}.png') for i in range(1,4)]
imgDance = [pygame.image.load(f'WOT1990_set/Dance/dance_left({i}).png ') for i in range(0,8)]

imgBonuses = [pygame.image.load(f'WOT1990_set/images/bonus_star.png'),
              pygame.image.load(f'WOT1990_set/images/bonus_tank.png'),
              pygame.image.load(f'WOT1990_set/images/bonus_bomb.png')]

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My WOT1990 OD2024 KVO75")
pygame.display.set_icon(pygame.image.load('WOT1990_set/images/dom.png').convert_alpha())
clock = pygame.time.Clock()

MOVE_SPEED    = [1,2,2,1,2,3,3,2]
BULLET_SPEED  = [4,5,6,5,5,5,6,7]
BULLET_DAMAGE = [1,1,2,3,2,2,3,4]
SHOT_DELAY    = [60,50,30,40,30,25,25,30]

DIRECTS =[[0,-1], [1,0], [0,1], [-1,0]]

class UI:
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == "tank":
                pygame.draw.rect(screen, obj.color, (5+i*70, 5, 22, 22))
                text = fontUI.render(str(obj.rank), 1, 'white')
                rect = text.get_rect(center=(5 + i*70 + 11, 5 + 11))
                screen.blit(text, rect)
                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center = (5 + i*70 + 32, 5+11))
                screen.blit(text, rect)
                i+=1

class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE-2, TILE-2)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5

        self.bulletSpeed =  5
        self.bulletDamage = 1
        self.shotTimer =    0
        self.shotDelay = 60
        self.isMove = False

        self.keyLEFT  = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP    = keyList[2]
        self.keyDOWN  = keyList[3]
        self.keySHOT  = keyList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image,(self.image.get_width()-5, self.image.get_height()-5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]

        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
           self.rect.x -= self.moveSpeed
           self.direct = 3
           self.isMove = True
        elif keys[self.keyRIGHT]:
           self.rect.x += self.moveSpeed
           self.direct = 1
           self.isMove = True
        elif keys[self.keyUP]:
           self.rect.y -= self.moveSpeed
           self.direct = 0
           self.isMove = True
        elif keys[self.keyDOWN]:
           self.rect.y += self.moveSpeed
           self.direct = 2
           self.isMove = True
        else: self.isMove = False

        if self.rect.y < 0 : self.rect.y = height
        if self.rect.y > height: self.rect.y = 0
        if self.rect.x < 0: self.rect.x = width
        if self.rect.x > width: self.rect.x = 0

        for obj in objects:
            if obj != self and obj.type =='block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            sound_effect1.play()
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1


    def draw(self):
        screen.blit(self.image, self.rect)
        '''
        pygame.draw.rect(screen, self.color, self.rect )
        x = self.rect.centerx + DIRECTS[self.direct][0] * 20
        y = self.rect.centery + DIRECTS[self.direct][1] * 20
        pygame.draw.line(screen, 'white', self.rect.center, (x,y) ,4 )
        '''
    def damage(self, value):
        self.hp -= value
        if self.hp <= 0 :
            objects.remove(self)

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py, self.dx, self.dy = px, py, dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.py < 0 or self.px > width or self.py > height:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type !='dance' and obj.type !='bang' and obj.type !='bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        sound_effect2.play()
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break

    def draw(self):
        pygame.draw.circle(screen, "yellow", (self.px, self.py),2)


class Dance:
    def __init__(self):
        objects.append(self)
        self.type = "dance"
        self.direction = 1 # 1 on the left direction, -1 on the right
        self.frame = 0
        self.px = -200

    def update(self):
        self.px += self.direction * 2
        if self.px >= width +200 : self.direction = -1
        if self.px <= -200 : self.direction = 1
        self.frame += 0.2
        if self.frame > 7: self.frame = 0

    def draw(self):
        image = imgDance[int(self.frame)]
        rect_d = image.get_rect(center=(self.px, height-150))
        if self.direction == -1:
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, rect_d)

class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = "bang"
        self.px, self.py = px, py
        self.frame = 0
    def update(self):
        self.frame +=0.2
        if self.frame >=3: objects.remove(self)
    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center = (self.px, self.py))
        screen.blit(image, rect)

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px,py,size,size)
        self.hp =1
    def update(self):
        pass
    def draw(self):
        screen.blit(imgBrick,self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0 : objects.remove(self)

class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'

        self.px, self.py = px, py
        self.bonusNum = bonusNum
        self.timer = 600

        self.image = imgBonuses[self.bonusNum]
        self.rect = self.image.get_rect(center = (self.px, self.py))
    def update(self):
        if self.timer > 0 : self.timer -=1
        else: objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(imgTanks)-1:
                        obj.rank +=1
                        objects.remove(self)
                        sndLive.play()
                        break
                elif self.bonusNum == 1:
                    obj.hp +=1
                    objects.remove(self)
                    sndStar.play()
                    break
                elif self.bonusNum == 2:
                    obj.hp -=1
                    objects.remove(self)
                    Bang(self.px, self.py)
                    sound_effect2.play()
                    break
    def draw(self):
        if self.timer % 30 < 15:
            screen.blit(self.image, self.rect)

def restart_game():
    global objects, bullets, ui, bonusTimer, timer, isMove, isWin, y
    bullets = []
    objects = []
    Tank('red', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_v))
    Tank('blue', 600, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))
    ui = UI()

    for _ in range(100):
        while True:
            x = randint(0, width // TILE - 1) * TILE
            y = randint(1, height // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            fined = False
            for obj in objects:
                if rect.colliderect(obj.rect): fined = True
            if fined == False: break
        Block(x, y, TILE)

    sound_effect1.play()
    pygame.mixer.music.load('sound_set/GTA.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    bonusTimer = 180
    timer = 0
    isMove = False
    isWin = False
    y = 0

restart_game()

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and t == 1:
                restart_game()
    # TANK
    keys = pygame.key.get_pressed()

    timer +=1
    if timer >= 260 and  not isWin:
        if oldIsMove != isMove:
            if isMove:
                sndMove.play()
                sndEngine.stop()
            else:
                sndMove.stop()
                sndEngine.play(-1)
    oldIsMove = isMove
    isMove = False

    for obj in objects:
        if obj.type == 'tank': isMove = isMove or obj.isMove


    if bonusTimer > 0 : bonusTimer -= 1
    elif t != 1:
        Bonus(randint(50,width-50), randint(50, height-50), randint(0, len(imgBonuses)-1))
        bonusTimer = randint(120,240)

    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()
    ui.update()

    screen.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()

    t=0 # Если остался 1 танк
    for obj in objects:
        if obj.type == "tank":
            t+=1
            tankWin = obj

    if t == 1 and not isWin:
        isWin, timer = True, 1000

    if t==1:
        pygame.draw.rect(screen, 'black', (width//2-200,height//2-180,width//2+1,height//2-130))
        pygame.draw.rect(screen, 'orange', (width//2-200, height//2-180, width//2+1, height//2-130),20)
        text = fontBig.render('WINNER !',1,tankWin.color)
        rect = text.get_rect(center=(width//2,height//2-100))
        screen.blit(text, rect)
        text = fontUI.render('Press push "Space" for new game',1,'grey')
        rect = text.get_rect(center=(width//2,height//2-60))
        screen.blit(text, rect)


    if timer < 260:
        y +=1
        pygame.draw.rect(screen, 'black', (width//2-330,height//2-200+y,width//2+260,150))
        pygame.draw.rect(screen, 'orange', (width//2-330, height//2-200+y, width//2+260, 150),20)
        text = fontBig.render('World Of Tanks from 1990', 1, 'white')
        rect = text.get_rect(center=(width//2,height//2-120+y))
        screen.blit(text, rect)
        text = fontUA.render("'a,d,w,s + v' - first player       '←,→,↓,↑' + Enter - second player", 1, 'grey')
        rect = text.get_rect(center=(width // 2 - 10, height // 2 - 90+y  ))
        screen.blit(text, rect)
        text = fontUA.render("КВО1975 - OD_1/05/2024", 1, 'grey')
        rect = text.get_rect(center=(width // 2 - 10, height - 15))
        screen.blit(text, rect)


    if isWin and timer == 1000:
        sndMove.stop()
        sndEngine.stop()
        pygame.mixer.music.load('WOT1990_set/dance/Dance.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        Dance()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
