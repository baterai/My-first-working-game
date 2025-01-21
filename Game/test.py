import pygame 
import sys 
from random import randint

pygame.init() 

#frame
clock = pygame.time.Clock()

#window
screen = pygame.display.set_mode((1000, 600))

#sky background
sky_col = (61,141,255)
sky = pygame.Surface((1000, 600))
sky.fill(sky_col)

#ground
ground = pygame.Surface((1000, 250))
ground.fill('Green')

#gravity
gravity = 0

#jump button
jump_button = pygame.transform.scale(pygame.image.load("game assets/Banana.png"), (50, 50)).convert_alpha()
jump_rect = jump_button.get_rect(center = (500, 570))

#score
font = pygame.Font("game assets\ARCADECLASSIC.TTF", 40)

def Score():
	current_time = int(pygame.time.get_ticks() / 1000) - score_start
	score_text = font.render(f"SCORE {current_time}", False, 'Black')
	score_rect = score_text.get_rect(center = (500, 50))
	screen.blit(score_text, score_rect)
	return current_time

score_start = 0
score = 0

#game over
game_over = pygame.Surface((1000, 530))
game_over.fill('Black')

gameover_font = pygame.Font("game assets\ARCADECLASSIC.TTF", 110)
gameover_text = gameover_font.render("GAME OVER", False, 'White')
gameover_text_rect = gameover_text.get_rect(center = (500, 300))


#ufo
aa = pygame.transform.scale(pygame.image.load("game assets/enemybullet1.png"), (20, 20)).convert_alpha()
aa_rect = aa.get_rect(center = (500, 300))


ufo1 = pygame.transform.scale(pygame.image.load("game assets/ufo_animation/UFO_animation1.png"), (100, 50)).convert_alpha()
ufo2 = pygame.transform.scale(pygame.image.load("game assets/ufo_animation/UFO_animation2.png"), (100, 50)).convert_alpha()
ufo3 = pygame.transform.scale(pygame.image.load("game assets/ufo_animation/UFO_animation3.png"), (100, 50)).convert_alpha()
ufo_mask = pygame.mask.from_surface(ufo1)
ufo_rect = ufo_mask.get_rect(midbottom = (150, 300))

ufo_animation = [ufo1, ufo2, ufo3]
ufo_index = 0

ufo = ufo_animation[ufo_index]

#ufo animation
def ufo_movement():
	global ufo_index, ufo

	ufo_index += 0.1
	if ufo_index >= len(ufo_animation):
		ufo_index = 0
	ufo = ufo_animation[int(ufo_index)]



#enemy
enemy = pygame.transform.scale(pygame.image.load("game assets/enemy.png"), (50, 50)).convert_alpha()
enemy_mask = pygame.mask.from_surface(enemy)


#def enemy_movement(enemy_list):
	#if enemy_list:
		#for enemy_spawn in enemy:
			#enemy_spawn.x -= 5
				
			#screen.blit(enemy, enemy_spawn)
		#enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
		#return enemy_list
		
	
	#else:
		#return []
	
#collide
def collide(enemy):
	if enemy:
		for enemy_spawn in enemy:
			if ufo_rect.colliderect(enemy_spawn):
				return False		
	return True
	


enemy_list = []

#Timer
enemy_timer = pygame.USEREVENT + 1
enemy_timer2 = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, 900)
pygame.time.set_timer(enemy_timer2, 2000)


#game while loop
run = True
game_active = True

while run:
	clock.tick(60)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
        		run = False    
		
		#if event.type == pygame.MOUSEMOTION:
			#print(event.pos)
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if jump_rect.collidepoint(event.pos):
					gravity = -15

			if event.type == enemy_timer:
				enemy_list.append(enemy_mask.get_rect(bottomleft = (randint(1200, 2000), randint(80, 500))))


		


	if game_active:
		#background
		screen.blit(sky, (0, 0))
		screen.blit(ground, (0, 530))
		#pygame.draw.line(screen,'Red',text_rect.topleft, text_rect.bottomright)
		
		#enemy
		#enemy_rect.left -= 5
		#enemy_list = enemy_movement(enemy_list)
		#if enemy_rect.right < 0:
			#enemy_rect.left = 1000
		
		

		#jump
		screen.blit(jump_button, jump_rect)
		screen.blit(aa, aa_rect)
		ufo_rect.y += gravity

		#ufo
		if ufo_rect.bottom < 540:
			gravity += 3
		ufo_rect.y += gravity
		if ufo_rect.bottom >= 540:
			ufo_rect.bottom = 540
		if ufo_rect.top <= 0:
			ufo_rect.top = 0
		ufo_movement()
		screen.blit(ufo, ufo_rect)

		if ufo_rect.bottom >= 540:
			gravity = 0
		if gravity >= 1:
			gravity = 0

		#collide
		#game_active = collide(enemy_list)


		#score
		score = Score()

	else:
		screen.blit(game_over, (0,0))
		screen.blit(gameover_text, gameover_text_rect)
		gameover_score = font.render(f"YOUR SCORE {score}", False, 'White')
		gameover_score_rect = gameover_score.get_rect(center = (500, 100))
		screen.blit(gameover_score, gameover_score_rect)

		key = pygame.key.get_pressed()
		
		if key[pygame.K_r]:
			score_start = int(pygame.time.get_ticks() / 1000)
			game_active = True
			enemy_list.clear()
			
			


	

	pygame.display.update()
	
pygame.quit()
quit()
