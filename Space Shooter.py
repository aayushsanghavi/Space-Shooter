#Shmup Game
#importing required libraries
import pygame
import random
import os

#setting constants
width = 450
height = 600
FPS = 60

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

font_name = pygame.font.match_font('sans')
def add_text(surface,text,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,True,white)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surface.blit(text_surface,text_rect)

def spawn_mob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

def lose_life():
	if player.shield <= 0:
		blast_sounds[3].play()
		player.hide()
		player.lives -= 1
		player.shield = 100
	
def draw_shield(surface,x,y,shield):
	if shield < 0:
		shield = 0
	bar_length = 100
	bar_height = 10
	bar_fill = (shield*bar_length)/100
	bar_outline = pygame.Rect(x,y,bar_length,bar_height)
	bar_filled = pygame.Rect(x,y,bar_fill,bar_height)
	pygame.draw.rect(surface,white,bar_outline,2)
	pygame.draw.rect(surface,green,bar_filled)

def draw_lives(surface,x,y,lives,life):
	for i in range(lives):
		life_rect = life.get_rect()
		life_rect.x += x
		life_rect.y = y + 0.08*height*i
		surface.blit(life,life_rect)

def game_over_screen():
	add_text(screen,"Space Shooter",60,width/2,0.25*height)
	add_text(screen,"Controls -",30,width/2,0.35*height)
	add_text(screen,"Cursor keys and W-A-S-D for movement",20,width/2,0.45*height)
	add_text(screen,"Space for shooting",20,width/2,height/2)
	add_text(screen,"Press Enter to start",20,width/2,0.6*height)
	pygame.display.flip()
	start = False
	while not start:
		clock.tick(FPS)
		keystate = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				start = True

class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img,(48,36))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.radius = 18
		self.rect.centerx = width/2
		self.rect.bottom = height - 0.03*height
		self.speedx = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()

	def update(self):
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1200:
			self.hidden = False
			self.rect.centerx = width/2
			self.rect.bottom = height - 0.03*height

		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
			self.speedx = 5
		if keystate[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx

		if self.rect.right > width:
			self.rect.right = width
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx,self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)
			bullet_sound.play()

	def hide(self):
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (width/2,2*height)

class Mob(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_original = random.choice(mob_images)
		self.image_original.set_colorkey(black)
		self.image = self.image_original.copy()	
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width*0.9 / 2)
		self.rect.x = random.randrange(0,width-self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedx = random.randrange(-2,2)
		self.speedy = random.randrange(3,8)
		self.rotation = 0
		self.rotation_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rotation = (self.rotation + self.rotation_speed) % 360
			new_image = pygame.transform.rotate(self.image_original,self.rotation)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy		
		if self.rect.top > height+10 or self.rect.left < -20 or self.rect.right > width+20 :
			self.rect.x = random.randrange(0,width-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(2,7)

class Ufo(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(ufo_img,(50,50))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.x = width/8 + (2*width*random.random())/3		
		self.rect.y = height/3 + height/2*random.random()
		self.radius = 25
		self.speedx = 2
		self.hide_timer = pygame.time.get_ticks()
		self.hidden = False
		self.shoot_timer = 0
		self.shield = 100
		
	def update(self):
		self.rect.x += self.speedx	
		if self.rect.x <= 0.1*width:
			self.speedx = 2
		elif self.rect.x >= 0.8*width:
			self.speedx = -2
	
		self.shoot_timer += 1
		if self.shoot_timer == 15:
			self.shoot_timer = 0
			self.shoot()

		now = pygame.time.get_ticks()
		if now - self.hide_timer > 4000 or self.shield == 0:
			self.hidden = False
			self.hide_timer = pygame.time.get_ticks()
			self.rect.y = height/10 + (2*height*random.random())/5
			self.rect.x = width/8 + (2*width*random.random())/3
			self.kill()
			self.shield = 100
			
	def shoot(self):
		missile = Missile(self.rect.centerx,self.rect.top)
		all_sprites.add(missile)
		missiles.add(missile)
		missile_sound.play()

class Missile(pygame.sprite.Sprite):
	
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(missile_img,(9,25))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.speedy = 10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > height:
			self.kill()

class Bullet(pygame.sprite.Sprite):

	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(bullet_img,(6,36))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Powerup(pygame.sprite.Sprite):

	def __init__(self,category):
		pygame.sprite.Sprite.__init__(self)
		self.category = category
		self.image = powerup_images[category]
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0,width-self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = 3
		self.category = category
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > height*1.05:
			self.kill()

class Explosion(pygame.sprite.Sprite):

	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_animation[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 80

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_animation[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_animation[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

#initialising pygame and sound
pygame.init()
pygame.mixer.init()

#creating up the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

#set up game assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
sound_folder = os.path.join(game_folder,"sound")
background = pygame.image.load(os.path.join(img_folder,"stars.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder,"playerShip1_orange.png")).convert()
ufo_img = pygame.image.load(os.path.join(img_folder,"ufoRed.png")).convert()
player_life = pygame.image.load(os.path.join(img_folder,"playerLife1_orange.png")).convert()
player_life.set_colorkey(black)
bullet_img = pygame.image.load(os.path.join(img_folder,"laserGreen13.png")).convert()
missile_img = pygame.image.load(os.path.join(img_folder,"laserBlue06.png")).convert()
mob_type = ["meteorBrown_med1.png","meteorBrown_med2.png","meteorBrown_small1.png",
			"meteorBrown_small2.png","meteorBrown_tiny1.png","meteorBrown_tiny2.png"]
mob_images = []
for i in mob_type:
	mob_images.append(pygame.image.load(os.path.join(img_folder,i)).convert())
powerup_type = ["shield_bronze.png","shield_silver.png","shield_gold.png","playerLife1_orange.png"
				,"bolt_bronze.png","bolt_silver.png","bolt_gold.png"]
powerup_images = []
for i in powerup_type:
	powerup_images.append(pygame.image.load(os.path.join(img_folder,i)).convert())

explosion_animation = {}
explosion_animation['large'] = []
explosion_animation['small'] = []
explosion_animation['player'] = []

for i in range(9):
	filename = 'regularExplosion0{}.png'.format(i)
	explosion_img = pygame.image.load(os.path.join(img_folder,filename)).convert()
	explosion_img.set_colorkey(black)
	explosion_img_large = pygame.transform.scale(explosion_img,(70,70))
	explosion_animation['large'].append(explosion_img_large)
	explosion_img_small = pygame.transform.scale(explosion_img,(30,30))
	explosion_animation['small'].append(explosion_img_small)

	filename = 'sonicExplosion0{}.png'.format(i)
	explosion_img = pygame.image.load(os.path.join(img_folder,filename)).convert()
	explosion_img.set_colorkey(black)
	explosion_animation['player'].append(explosion_img)

bullet_sound = pygame.mixer.Sound(os.path.join(sound_folder,"Laser_Shoot.wav"))
bullet_sound.set_volume(0.3)
missile_sound = pygame.mixer.Sound(os.path.join(sound_folder,"Missile_Shoot.wav"))
missile_sound.set_volume(0.3)
ufo_sound = pygame.mixer.Sound(os.path.join(sound_folder,"Ufo_spawn.wav"))
powerup_sound = pygame.mixer.Sound(os.path.join(sound_folder,"powerUp.ogg"))
powerup_sound.set_volume(2)
blast_type = ["Explosion_tiny.wav","Explosion_small.wav","Explosion_med.wav","Explosion_player.ogg"]
blast_sounds = []
for i in blast_type:
	blast_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder,i)))
pygame.mixer.music.load(os.path.join(sound_folder,'Harp_Battle_Song.mp3'))

pygame.mixer.music.play(-1)

#game loop
running = True
game_over = True

while running:
	
	if game_over:
		game_over_screen()
		game_over = False
		score = 0
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		missiles = pygame.sprite.Group()
		player = Player()
		ufo = Ufo()
		all_sprites.add(player)
		for i in range(8):
			spawn_mob()

	if player.lives == 0 and not death_explosion.alive():
		game_over = False

	#keep running at fps
	clock.tick(FPS)

	#Event
	for event in pygame.event.get():
		#check for closing the window
		if event.type == pygame.QUIT:
			running = False

	#Update
	all_sprites.update()

	#checking to see if mobs hit the player
	hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
	for hit in hits:
		spawn_mob()
		explosion = Explosion(hit.rect.center,'small')
		all_sprites.add(explosion)
		blast_sounds[2].play()
		if hit.radius < 10:
			player.shield -= 10
		elif hit.radius > 10 and hit.radius < 15:
			player.shield -= 20
		elif hit.radius > 15 and hit.radius < 20:
			player.shield -= 25

		if player.shield <= 0:
			death_explosion = Explosion(player.rect.center,'player')
			all_sprites.add(death_explosion)
		lose_life()

	if player.lives == 0 and not death_explosion.alive():
		game_over = False

	claps = pygame.sprite.spritecollide(player,missiles,True,pygame.sprite.collide_circle)
	for clap in claps:
		explosion = Explosion(clap.rect.center,'small')
		all_sprites.add(explosion)
		blast_sounds[2].play()
		player.shield -= 25

		if player.shield <= 0:
			death_explosion = Explosion(player.rect.center,'player')
			all_sprites.add(death_explosion)
		lose_life()

	
	#checking to see if mobs hit the player
	blasts = pygame.sprite.groupcollide(mobs,bullets,True,True)
	explosion = {}
	for blast in blasts:
		if blast.radius < 10:
			score += 5
			explosion = Explosion(blast.rect.center,'small')
			blast_sounds[0].play()
		elif blast.radius > 10 and blast.radius < 15:
			score += 3
			explosion = Explosion(blast.rect.center,'small')
			blast_sounds[1].play()
		elif blast.radius > 15 and blast.radius < 20:
			score += 1
			explosion = Explosion(blast.rect.center,'large')
			blast_sounds[2].play()
		
		all_sprites.add(explosion)
		spawn_mob()

		if random.random() >= 0.93:
			powerup = Powerup(random.randint(1,7)-1)
			all_sprites.add(powerup)
			powerups.add(powerup)

	booms = pygame.sprite.spritecollide(ufo,bullets,True,pygame.sprite.collide_circle)
	for boom in booms:
		ufo.shield -= 15
		explosion = Explosion(boom.rect.center,'small')
		all_sprites.add(explosion)
		blast_sounds[1].play()

	collects = pygame.sprite.spritecollide(player,powerups,True)
	for collect in collects:
		powerup_sound.play()
		if collect.category <= 2:
			player.shield += (collect.category+1)*10
			if player.shield >= 100:
				player.shield = 100
		if collect.category == 3:
			player.lives += 1
			if player.lives >= 3:
				player.lives = 3
		if collect.category >= 4:
			for mob in mobs:
				if mob.rect.y < height/3:
					explosion = Explosion(mob.rect.center,'large')
					blast_sounds[2].play()
					all_sprites.add(explosion)
		if collect.category >= 5:
			for mob in mobs:
				if mob.rect.y < (2*height)/3:
					explosion = Explosion(mob.rect.center,'large')
					blast_sounds[2].play()
					all_sprites.add(explosion)
		if collect.category >= 6:
			for mob in mobs:
				if mob.rect.y < height:
					explosion = Explosion(mob.rect.center,'large')
					blast_sounds[2].play()
					all_sprites.add(explosion)

	if score % 400 >= 375 and not ufo.hidden:
		ufo_sound.play()
		all_sprites.add(ufo)
		ufo.hidden = True

	#Draw and render
	screen.fill(black)
	screen.blit(background,background_rect)
	all_sprites.draw(screen)
	add_text(screen,str(score),30,width/2,height-0.99*height)
	draw_shield(screen,5,5,player.shield)
	draw_lives(screen,width-0.1*width,height-0.6*height,player.lives,player_life)
	#after drawing the next frame we flip the display
	pygame.display.flip()

pygame.quit()