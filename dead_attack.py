import time, sys
from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 8:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 100:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 8:
            self.rect.y -= self.speed 
        if keys[K_DOWN] and self.rect.y < win_width - 100:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -30)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(100, win_width - 100)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat ='{:02d}: {:02d}'.format
        (mins, secs)
        print(timeformat, end='\r')
        time.delay(1)
        time_sec -= 1

win_width = 1280
win_height = 720
window = display.set_mode(
    (win_width, win_height)
)
display.set_caption("Shooter")
background = transform.scale(
    image.load("assets/zombies/sprites/road_image.png"),
    (win_width, win_height)
)

player = "assets/zombies/sprites/player_image.png"
img_enemy = "assets/zombies/sprites/zombie_image.png"
img_bullet = "assets/zombies/sprites/bullet.png"

score = 0
lost = 0
max_lost = 3
goal = 500
ammo = 20
shotscount = 0
gamewave = 1
lastwave = 6

mixer.init()
mixer.music.load('assets/zombies/music/start.mp3')
mixer.music.play()

fire_sound = mixer.Sound("assets/zombies/sound/fire.mp3")
hitsound1 = mixer.Sound("assets/zombies/sound/hit1.mp3")
hitsound2 = mixer.Sound("assets/zombies/sound/hit2.mp3")
losemusic = mixer.Sound("assets/zombies/music/lose.mp3")
reloadsound = mixer.Sound("assets/zombies/sound/reload.mp3")

font.init()
font4 = font.SysFont("Fixedsys", 40)
font3 = font.SysFont("Fixedsys", 55)
font2 = font.SysFont("Fixedsys", 70)
font1 = font.SysFont("Fixedsys ", 46)
win = font1.render("YOU WIN!", True, (128, 209, 255))
lose = font2.render("YOU LOSE.", True, (180,0, 0))


run = True
finish = False
clock = time.Clock()
FPS = 30
ship = Player(player, 5, win_height - 100, 100, 100, 20)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        100, win_width - 100), -40, 80, 80, randint(2, 10))
    monsters.add(monster)

bullets = sprite.Group()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if ammo > 0:
                    fire_sound.play()
                    ship.fire()
                    ammo = ammo - 1
                    shotscount = shotscount + 1
                if ammo <= 0:
                    reloadsound.play()
                    ammo += 4
                    ammo += 4
                    ammo += 4
                    ammo += 4
                    ammo += 4
                    reloadsound.play()
            if e.key == K_ESCAPE:
                sys.exit()



    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), 1, (55, 255, 5))
        window.blit(text, (10, 10))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 75, 0))
        window.blit(text_lose, (10, 60))
        text_goal = font2.render("Ціль:" + str(goal), 1, (255, 255, 255))
        window.blit(text_goal, (10, 125))
        text_ammo = font3.render(str(ammo) + "/20", 1, (255, 180, 0))
        window.blit(text_ammo, (950, 560))
        text_goal = font4.render("Постріли:" + str(shotscount), 1, (255, 255, 255))
        window.blit(text_goal, (1100, 530))
        text_goal = font4.render("Раунд:" + str(gamewave), 1, (255, 255, 255))
        window.blit(text_goal, (1120, 490))


        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()


        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            randomsound = randint(1, 2)
            if randomsound == 1:
                hitsound1.play()
                score = score + 10
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(2, 10))
                monsters.add(monster)

            if randomsound == 2:
                hitsound2.play()
                score = score + 10
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 80, randint(2, 10))
                monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            mixer.music.stop()
            losemusic.play()
            hitsound2.stop()
            hitsound1.stop()
            window.blit(lose, (640, 360))
        if gamewave >= lastwave:
            finish = True
            hitsound2.stop()
            hitsound1.stop()
            window.blit(win, (640, 360))
        if score >= goal:
            gamewave += 1
            goal += 500

        display.update()
    time.delay(30)   

