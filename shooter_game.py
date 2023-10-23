from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
        self.size_x=size_x
        self.size_y=size_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet=Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
        
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0

health = 120
score = 0
lost = 0
clock = time.Clock()
FPS = 60
win_width = 700
win_height = 500
ammo = 0
reload_time = False

font.init()
font2=font.Font(None,36)
font1=font.Font(None,80)

window = display.set_mode((win_width,win_height))
display.set_caption("Shooter game")
background=transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
player=Player("rocket.png",100,400,80,100,7)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png",randint(80,win_width-80),-10,80,50,randint(1,5))
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid("asteroid.png",randint(80,win_width-80),-10,80,50,randint(1,7))
    asteroids.add(asteroid)


game = True
finish = False

while game: 
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if ammo < 6 and reload_time == False:
                    player.fire()
                    ammo += 1
                if ammo >= 6 and reload_time == False:
                    last_time = timer()
                    reload_time = True

    if not finish:
        window.blit(background,(0,0))
        text=font2.render("Score: " + str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text1=font2.render("Missed: " + str(lost),1,(255,255,255))
        window.blit(text1,(10,50))
        text3=font1.render("You win",1,(0,255,0))
        text4=font1.render("You lose",1,(255,0,0))
        text5=font2.render("Health: " + str(health),1,(200,200,200))
        window.blit(text5,(500,50))
        player.reset()
        player.update()  
        monsters.draw(window)
        monsters.update()
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        collides = sprite.groupcollide(bullets,monsters,True,True)
        
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload=font2.render("Reloading...",1,(150,150,150))
                window.blit(reload,(200,400))
            else:
                ammo = 0
                reload_time = False
                
        for i in collides:
            score += 1
            monster = Enemy("ufo.png",randint(80,win_width-80),-10,80,50,randint(1,5))
            monsters.add(monster)
        
        if sprite.spritecollide(player,monsters,True):
            health = health - 40
            monster = Enemy("ufo.png",randint(80,win_width-80),-10,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(player,asteroids,True):
            health = health - 40
            asteroid = Asteroid("asteroid.png",randint(80,win_width-80),-10,80,50,randint(1,7))
            asteroids.add(asteroid)

        if health <= 0 or lost >= 3:
            finish = True
            window.blit(text4,(200,200))
       
        if score > 9:
            finish = True
            window.blit(text3,(200,200))       
        
        display.update()
    
    else:
        finish = False
        score = 0
        lost = 0
        health = 120
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for asteroid in asteroids:
            asteroid.kill()
        time.delay(3000)
        for i in range(5):
            monster=Enemy("ufo.png",randint(80,win_width-80),-10,80,50,randint(1,5))
            monsters.add(monster)
        for i in range(3):
            asteroid=Asteroid("asteroid.png",randint(80,win_width-80),-10,80,50,randint(1,7))
            asteroids.add(asteroid)
        

    time.delay(25)
