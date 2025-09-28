from random import randint
from pygame import *
import time as t
window = display.set_mode((700, 500))
display.set_caption("Shooter")
bg = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
Finish = False
run = True
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
       super().__init__()
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
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 65:
            self.rect.x += self.speed     
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20 , 15)
        Bullets.add(bullet)
lost = 0 
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = (randint(0, 700-80))
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 500:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -20
            self.rect.x = randint(0, 700-80)

Bullets = sprite.Group()
ship = Player('rocket.png', 5 , 400, 80 ,100, 10)
ammo = 10
reloading = False
reload_time = 0
nyawa = 3

monster1 = Enemy('ufo.png', randint (0, 620), -40, 50, 80, randint(1,5))
monster2 = Enemy('ufo.png', randint (0, 620), -40, 50, 80, randint(1,5))
monster3 = Enemy('ufo.png', randint (0, 620), -40, 50, 80, randint(1,5))
monster4 = Enemy('ufo.png', randint (0, 620), -40, 50, 80, randint(1,5))
monster5 = Enemy('ufo.png', randint (0, 620), -40, 50, 80, randint(1,5))

asteroid1 = Asteroid('asteroid.png', randint(0,620), -40, 50, 80, randint(1,5))
asteroid2 = Asteroid('asteroid.png', randint(0,620), -40, 50, 80, randint(1,5))
asteroid3 = Asteroid('asteroid.png', randint(0,620), -40, 50, 80, randint(1,5))

asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)

monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

font.init()
font2 = font.Font(None, 36)
score = 0
while run:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_f:
                if ammo > 0 and reloading == False:
                    ship.fire()
                    fire_sound.play()
                    ammo -= 1
    if not Finish:
        window.blit(bg, (0,0))
        collides = sprite.groupcollide(monsters, Bullets, True, True)
        if collides:
            monster = Enemy('ufo.png', randint(0,620), -40,80,50, randint(1,5))
            monsters.add(monster)
            score += 1
        text_lost = font2.render("Missed : "+ str(lost), 1, (255, 255, 255))
        text_score = font2.render("Score  : " + str(score), 1, (255, 255, 255))
        text_nyawa = font2.render("Life  : " +str(nyawa), 1, (255, 255, 255))
        window.blit(text_nyawa, (600,20))
        if score == 10:
            Finish = True
            text_win = font2.render("You Win!", 1, (255,255,255))
            window.blit(text_win, (200,200))
        if sprite.spritecollide(ship, asteroids, True):
            nyawa -= 1
        if sprite.spritecollide(ship, monsters, True):
            nyawa -= 1
        if lost > 3 :
            Finish = True
            text_lose = font2.render("You lose!", 1, (255, 255, 255))
            window.blit(text_lose, (200,200))
        if nyawa < 1:
            Finish = True
            text_lose = font2.render("You lose!", 1, (255,255,255))
            window.blit(text_lose, (200,200))
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(text_lost, (10,50))
        window.blit(text_score, (10,20))
        Bullets.draw(window)
        Bullets.update()
        if ammo == 0 and reloading == False:
            reloading = True
            start = t.time()
        if reloading:
            text_reload = font2.render("Reloading!", 1, (255, 255, 255))
            window.blit(text_reload, (300, 450))
            reload_time = t.time() - start
        if reload_time > 1:
            reloading = False
            reload_time = 0
            ammo = 10

    display.update()
font = font.SysFont('Arial', 40)
# 