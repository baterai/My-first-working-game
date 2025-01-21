import pygame
import pygame.display
import pygame.display
from pygame.locals import *
from pygame.sprite import Group
import random


pygame.mixer.init(44100, 16, 2, 4096)
pygame.mixer.set_num_channels(16)
pygame.init()

#framerate
clock = pygame.time.Clock()
fps = 60

#window scale
width = 600
height = 650

#window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Legacy of Dumspter Hero')

#game menu
background_titlescreen = pygame.Surface((width, height))
background_titlescreen.fill('Black')

startbutton_colour = pygame.Surface((150, 50))
startbutton_colour.fill('Green')
startbutton_rect = startbutton_colour.get_rect(center = (300, 400))

quitbutton_colour = pygame.Surface((150, 50))
quitbutton_colour.fill('Red')
quitbutton_rect = quitbutton_colour.get_rect(center = (300, 500))

#background
bg = pygame.transform.scale(pygame.image.load("game assets\image\Background.jpg"), (width, height))

def draw_bg():
    screen.blit(bg, (0, 0))

#text
font30 = pygame.Font("game assets/font/ARCADECLASSIC.TTF", 30)
font40 = pygame.Font("game assets/font/ARCADECLASSIC.TTF", 40)
font50 = pygame.Font("game assets/font/ARCADECLASSIC.TTF", 50)

fontscr = pygame.font.SysFont("Times New Roman", 40)
fonttitle = pygame.font.SysFont("Times New Roman", 50)

black = (0, 0, 0)
white = (255, 255, 255)


def create_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#game over
gameover_screen = pygame.Surface((width, height))
gameover_screen.fill("Black")

#music
background_channel = pygame.mixer.Channel(1)
menu_channel = pygame.mixer.Channel(2)
winning_channel = pygame.mixer.Channel(3)
explosion_channel = pygame.mixer.Channel(4)
    
background_music = pygame.mixer.Sound("game assets/sound/background_music.wav")
menu_music = pygame.mixer.Sound("game assets/sound/menu_music.ogg")
winning_sound = pygame.mixer.Sound("game assets/sound/winning.ogg")
explosion_sound = pygame.mixer.Sound("game assets/sound/explosion.wav")


#player
class Trashcan(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("game assets/image/player/Trashcan.webp"), (100, 100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        explosion1 = pygame.transform.scale(pygame.image.load("game assets/image/player/explosion-01.png"), (100, 100)).convert_alpha()
        explosion2 = pygame.transform.scale(pygame.image.load("game assets/image/player/explosion-02.png"), (100, 100)).convert_alpha()
        explosion3 = pygame.transform.scale(pygame.image.load("game assets/image/player/explosion-03.png"), (100, 100)).convert_alpha()
        self.index = 0
        self.explosion_frame = [explosion1, explosion2, explosion3]
        self.explosion = self.explosion_frame[self.index]
        self.health = health
        self.health_left = health
        self.last_shot = pygame.time.get_ticks()
        self.shooting = False

    def input(self):
        speed = 10

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.rect.right < width + 20:
            self.rect.x += speed
        if key[pygame.K_LEFT] and self.rect.left > -12:
            self.rect.x -= speed

        self.mask = pygame.mask.from_surface(self.image)

    def Health(self):
        global game_over

        red = (255, 0, 0)
        green = (0, 255, 0)


        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom - 10), self.rect.width, 15))
        if self.health_left > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom - 10), int(self.rect.width * (self.health_left / self.health)), 15))
        elif self.health_left <= 0:
            self.kill()
            
            game_over -= 1
            enemies_grup.empty()

        return game_over

    def Shoot(self):
        time_now = pygame.time.get_ticks()

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and time_now - self.last_shot > 300 and not self.shooting:
            self.shooting = True
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_grup.add(bullet)
            self.last_shot = time_now

        elif not key[pygame.K_SPACE]:
            self.shooting = False

    def update(self):
        self.input()
        self.Health()
        self.Shoot()


        

#bullet
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("game assets/image/player/Banana.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        
        self.rect.y -= 20 

        if pygame.sprite.spritecollide(self, enemies_grup, True):
            score.obtain_score()
            self.kill()

        elif pygame.sprite.spritecollide(self, enemies2_grup, True):
            score.obtain_extrascore()
            self.kill()

        
        
        

            
        
        
        if self.rect.bottom < 0:
            self.kill()
        

    


#enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_frame1 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/enemy animation/enemy.png"), (50, 50)).convert_alpha()
        image_frame2 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/enemy animation/enemy2.png"), (50, 50)).convert_alpha()
        self.image_animation = [image_frame1, image_frame2]
        self.image_index = 0
        self.image = self.image_animation[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_sound = explosion_channel
        self.hit_sound.set_volume(0.3)

    def movement(self):
        speed = 3

        self.rect.y += speed

        if self.rect.top > height:
            self.kill()
        
        self.mask = pygame.mask.from_surface(self.image)

    def collide(self):
        if pygame.sprite.spritecollide(self, enemies_grup, False):
            pass
        if pygame.sprite.spritecollide(self, trashcan_grup, False):
            if pygame.sprite.spritecollide(self, trashcan_grup, False, pygame.sprite.collide_mask):
                self.kill()
                self.hit_sound.play(explosion_sound)

                trashcan.health_left -= 1

    def animation(self):
        self.image_index += 0.1

        if self.image_index >= len(self.image_animation):
            self.image_index = 0

        self.image = self.image_animation[int(self.image_index)]

    def update(self):
        self.movement()
        self.collide()
        self.animation()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_frame1 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/enemy animation/enemyshoot1.png"), (50, 50)).convert_alpha()
        image_frame2 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/enemy animation/enemyshoot2.png"), (50, 50)).convert_alpha()
        self.image_animation = [image_frame1, image_frame2]
        self.image_index = 0
        self.image = self.image_animation[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_sound = explosion_channel
        self.hit_sound.set_volume(0.3)
        self.last_shot = pygame.time.get_ticks()
        self.shooting = False

    def movement(self):
        speed = 3

        self.rect.y += speed

        if self.rect.top > height:
            self.kill()
        
        self.mask = pygame.mask.from_surface(self.image)

    def collide(self):
        if pygame.sprite.spritecollide(self, enemies_grup, False):
            pass
        if pygame.sprite.spritecollide(self, trashcan_grup, False):
            if pygame.sprite.spritecollide(self, trashcan_grup, False, pygame.sprite.collide_mask):
                self.kill()
                self.hit_sound.play(explosion_sound)
                trashcan.health_left -= 1

    def animation(self):
        self.image_index += 0.1

        if self.image_index >= len(self.image_animation):
            self.image_index = 0

        self.image = self.image_animation[int(self.image_index)]

    def shoot(self):
        time_now = pygame.time.get_ticks()

        if time_now - self.last_shot > 1000:
            self.shooting = True
            bullet = EnemyBullets(self.rect.centerx, self.rect.bottom)
            bullet_grup.add(bullet)
            self.last_shot = time_now

        else:
            self.shooting = False




    def update(self):
        self.movement()
        self.collide()
        self.animation()
        self.shoot()

#enemy bullet
class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_frame1 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/bullet animation/enemybullet1.png"), (20, 20)).convert_alpha()
        self.image_frame2 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/bullet animation/enemybullet2.png"), (20, 20)).convert_alpha()
        self.image_frame3 = pygame.transform.scale(pygame.image.load("game assets/image/enemy/bullet animation/enemybullet3.png"), (20, 20)).convert_alpha()
        self.image_animation = [self.image_frame1, self.image_frame2, self.image_frame3]
        self.image_index = 0
        self.image = self.image_animation[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.hit_sound = pygame.mixer.Sound("game assets/sound/explosion.wav")
        self.hit_sound.set_volume(0.3)
    
    def movement(self):
        
        self.rect.y += 10 

        if pygame.sprite.spritecollide(self, trashcan_grup, False):
            if pygame.sprite.spritecollide(self, trashcan_grup, False, pygame.sprite.collide_mask):
                self.kill()
                score.lose_score()
                self.hit_sound.play()
                trashcan.health_left -= 1
        else:
            pass 
        
        
        if self.rect.top > height:
            self.kill()

    def animation(self):
        self.image_index += 0.1

        if self.image_index >= len(self.image_animation):
            self.image_index = 0

        self.image = self.image_animation[int(self.image_index)]

    def update(self):
        self.movement()
        self.animation()

        
    


#score
class Score():
    def __init__(self, score, font, x, y):
        self.score = score
        self.font = font
        self.x = x
        self.y = y
        pygame.mixer.music.load("game assets/sound/winning.ogg")
        pygame.mixer.music.set_volume(0.3)

        
    

    def player_score(self):
        global game_over


        player_score = self.score

        score_surface = self.font.render(f"score:{str(player_score)}", True, white)
        screen.blit(score_surface, (self.x, self.y))

        if player_score == 300:
            game_over += 1
            pygame.mixer.music.play()
        
        return game_over
            

        
        
            
    
    def obtain_score(self):
        self.score += 10
    
    def obtain_extrascore(self):
        self.score += 20

    def lose_score(self):
        self.score -= 30
        self.score = max(0, self.score)


        
        



#countdown
countdown = 5
counter = pygame.time.get_ticks()


#add sprite
trashcan_grup = pygame.sprite.GroupSingle()
bullet_grup = pygame.sprite.Group()
enemies_grup = pygame.sprite.Group()
enemies2_grup = pygame.sprite.Group()
trashcan = Trashcan(int(width / 2), height - 100, 3)
trashcan_grup.add(trashcan)


def create_enemies():
    X_position = [100, 200,300, 400, 500]
    Y_position = [-100, -200, -300, -400]
    exist = []
    random.shuffle([X_position, Y_position])
    for a in range(6):
        while True:
            x = random.choice(X_position)
            y = random.choice(Y_position)

            if [x,y] not in exist:
                exist.append([x,y])
                enemies = Enemy(x, y)
                enemies_grup.add(enemies)
                

                break
    
    for b in range(4):
        while True:
            x = random.choice(X_position)
            y = random.choice(Y_position)

            if [x,y] not in exist:
                exist.append([x,y])
                enemies = Enemy2(x, y)
                enemies2_grup.add(enemies)
                

                break
    
    


#timer
class Timer:
    def __init__(self, duration, repeat = False, autostart = False, func = None):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.func = func
        if autostart:
            self.turn_on()

    def turn_on(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def turn_off(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.turn_on()

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time > self.duration:
                if self.func: self.func()
                self.turn_off()

#spawning
spawning = Timer(5000, autostart= True, repeat= True, func= create_enemies)

#player score
score = Score(0, fontscr, 10, 10)



        
#running game
Run = True
game_start = False
game_over = 0





while Run:

    clock.tick(fps)
    draw_bg()

    #draw sprite
    trashcan_grup.draw(screen)
    bullet_grup.draw(screen)

    enemies_grup.draw(screen)
    enemies2_grup.draw(screen)

    
    if game_start == False:

        screen.blit(background_titlescreen,(0, 0))
        create_text("LEGACY", fonttitle, white, int(width / 2 - 100), 30)
        create_text("OF", fonttitle, white, int(width / 2 - 30), 90)
        create_text("DUMSPTER HERO", fonttitle, white, 100, 150)
        



        screen.blit(startbutton_colour, startbutton_rect)
        create_text("PLAY", font40, black, int(width / 2 - 45), int(height / 2 + 55))

        screen.blit(quitbutton_colour, quitbutton_rect)
        create_text("QUIT", font40, black, int(width / 2 - 45), int(height / 2 + 155))

        create_text("CONTROL", font40, white, int(width - 550), int(height - 200))
        create_text("ARRROW KEY", font30, white, int(width - 550), int(height - 150))
        create_text("SPACEBAR", font30, white, int(width - 550), int(height - 130))

        if not menu_channel.get_busy():
            menu_channel.play(menu_music, -1)
            menu_channel.set_volume(0.2)


    else:
        

        if countdown == 0:
            if game_over == 0 :
                
                trashcan.update()

                spawning.update()
                
                for a in enemies_grup:
                    a.update()

                for b in enemies2_grup:
                    b.update()
                    
            
                bullet_grup.update()
                score.player_score()

                if not background_channel.get_busy():
                    background_channel.play(background_music)
                    background_channel.set_volume(0.2)
                

            else:
                if game_over == -1 :
                    background_channel.stop()
                    screen.blit(gameover_screen,(0, 0))
                    create_text("YOU  LOSE", font50, white, int(width/ 2 - 110), int(height/ 2 - 50))
                    create_text("PRESS  R  TO RESTART", font40, white, 120, int(height/ 2))
                    trashcan_grup.empty()
                    enemies_grup.empty()
                    enemies2_grup.empty()
                    bullet_grup.empty()
                    key = pygame.key.get_pressed()

                    if key[pygame.K_r]:
                        game_over = 0
                        countdown = 6
                        trashcan = Trashcan(int(width / 2), height - 100, 3)
                        trashcan_grup.add(trashcan)
                        spawning = Timer(5000, autostart= True, repeat= True, func= create_enemies)
                        score = Score(0, fontscr, 10, 10)
                        
                        
                    
                if game_over == 1 :
                    background_channel.stop()
                    screen.blit(gameover_screen,(0, 0))
                    create_text("YOU  WIN", font50, white, int(width/ 2 - 110), int(height/ 2 - 50))
                    create_text("PRESS  R  TO PLAY AGAIN", font40, white, 100, int(height/ 2))
                    trashcan_grup.empty()
                    enemies_grup.empty()
                    enemies2_grup.empty()
                    bullet_grup.empty()
                    key = pygame.key.get_pressed()
                    
                    
                  
                        
                        

                    if key[pygame.K_r]:
                        winning_channel.stop()
                        game_over = 0
                        countdown = 6
                        trashcan = Trashcan(int(width / 2), height - 100, 3)
                        trashcan_grup.add(trashcan)
                        spawning = Timer(5000, autostart= True, repeat= True, func= create_enemies)
                        score = Score(0, fontscr, 10, 10)



        if countdown > 0:
            create_text("ARE YOU READY", font50, black, int(width/ 2 - 160), int(height/ 2 - 50))
            create_text(str(countdown), font50, black, int(width/ 2 - 20), int(height/ 2))
            create_text("OBJECTION", font50, white, int(width/ 2 - 150), int(height - 600))
            create_text("HIT 300 SCORES", font40, white, int(width/ 2 - 150), int(height - 550))

            timer = pygame.time.get_ticks()
            if timer - counter > 1000:
                countdown -= 1
                counter = timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             Run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if startbutton_rect.collidepoint(event.pos):
                game_start = True
                menu_channel.stop()
            if quitbutton_rect.collidepoint(event.pos):
                Run = False


    pygame.display.update()


pygame.quit()