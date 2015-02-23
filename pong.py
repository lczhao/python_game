import pygame, sys;
from pygame.locals import *;
import random;

BLACK = (0, 0, 0);
WHITE = (255, 255, 255);
RED = (255, 0, 0);
GREEN = (0, 255, 0);
BLUE = (0, 0, 255);

class Wall(pygame.sprite.Sprite):
	def __init__(self,color, x, y, width, height):
		pygame.sprite.Sprite.__init__(self);	#parent constructor;
		
		self.image = pygame.Surface([width, height]);
		self.image.fill(color);
		
		self.rect = self.image.get_rect();
		self.rect.y = y;
		self.rect.x = x;

class Goal(Wall):
	def __init__(self,x,y, width, height):
		super().__init__(BLACK, x, y, width, height);

class Bar(Wall):
	change_x = 0;
	change_y = 0;
	score = 0;
	def __init__(self,x,y):
		super().__init__(GREEN, x, y, 10, 50);
	
	def change_speed(self, y):
		self.change_y += y;
	
	def update(self, walls):
		self.rect.y += self.change_y;
		block_hit_list = pygame.sprite.spritecollide(self, walls, False);
		
		for block in block_hit_list:
			#we are moving to the bottom
			if self.change_y > 0:
				self.rect.bottom = block.rect.top;	#block is at our right, block it;
			else:
				self.rect.top = block.rect.bottom;	 #block is at our left

class AI_Bar(Bar):
	change_x = 0;
	change_y = 0;
	def __init__(self,x,y):
		super().__init__(x,y);
	def judge(self, ball):
		if ball.rect.y >= self.rect.y:
			self.change_y = 3;
		else:
			self.change_y = -3;
			
class Pong(pygame.sprite.Sprite):
	
	change_x = 1;
	change_y = 1;
	
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self);
		
		self.image = pygame.Surface([15, 15]); #player is 15*15 px
		self.image.fill(WHITE);
		
		self.rect = self.image.get_rect();
		self.rect.y = y;
		self.rect.x = x;
		
		self.change_x = 0;
		self.change_y = 0;
	
	def move(self):
		self.change_x = random.randint(2, 5);
		self.change_y = random.randint(2, 4);
	
	def update(self, walls):
		#update the current coordinate
		self.rect.x += self.change_x;
		
		#False for not getting rid of any one
		block_hit_list = pygame.sprite.spritecollide(self, walls, False);	#get collide list
		
		for block in block_hit_list:
			#we are moving to the right
			if self.change_x > 0:
				self.rect.right = block.rect.left;	#block is at our right, block it;
				
			else:
				self.rect.left = block.rect.right;	 #block is at our left
			self.change_x = - self.change_x;
			
		self.rect.y += self.change_y;
		
		#do the same thing for y coordinate
		block_hit_list = pygame.sprite.spritecollide(self, walls, False);
		
		for block in block_hit_list:
			#we are moving down
			if self.change_y > 0:
				self.rect.bottom = block.rect.top;
			else:
				self.rect.top = block.rect.bottom;
			
			self.change_y = - self.change_y;

def main():
	pygame.init();
	
	FPS = 60;
	fpsClock = pygame.time.Clock();
	
	window_width = 500;
	window_height = 300;
	
	ball_start_x = 240;
	ball_start_y = 140;
	
	global game_start;		#To mark whether or not we display the welcome screen
	game_start = False;
	
	window = pygame.display.set_mode([window_width, window_height]);
	
	ball = Pong(ball_start_x, ball_start_y);	#init the ball;
	#ball.move(5, 3);		#set the initial velocity of the ball
	
	all_sprite_list = pygame.sprite.Group();		#pygame sprite lists
	#all_sprite_list.add(ball);
	
	#initialize our wall here..
	wall_list = pygame.sprite.Group();
	border = pygame.sprite.Group();
	
	wall = Wall(BLUE, 0, 0, 500, 10);
	wall_list.add(wall);
	border.add(wall);
	all_sprite_list.add(wall);
	
	wall = Wall(BLUE, 0, 290, 500, 10);
	wall_list.add(wall);
	border.add(wall);
	all_sprite_list.add(wall);
	
	#Initializing players ... 
	bar1 = Bar(20, 125);
	wall_list.add(bar1);
	all_sprite_list.add(bar1);
	
	bar2 = AI_Bar(470, 125)
	all_sprite_list.add(bar2);
	wall_list.add(bar2);
	
	done = False;
	
	#event loop ...
	while not done:
		for event in pygame.event.get():
			if event.type == QUIT:
				done = True;
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					bar1.change_speed(-5);
				elif event.key == K_DOWN:
					bar1.change_speed(5);
				elif event.key == K_SPACE:
					#reinitialize the game if pressed space
					all_sprite_list.remove(ball);
					ball = Pong(ball_start_x, ball_start_y);	
					ball.move();		
					all_sprite_list.add(ball);
					game_start = True;
			elif event.type == KEYUP:
				if event.key == K_UP:
					bar1.change_speed(5);
				elif event.key == K_DOWN:
					bar1.change_speed(-5);
		
		#update the coordinate of our game objects...
		ball.update(wall_list);
		
		bar1.update(border);
		bar2.judge(ball);
		bar2.update(border);
		
		#redraw the whole thing
		window.fill(BLACK);
		all_sprite_list.draw(window);
		
		pygame.display.flip();
		
		#FPS = 60
		fpsClock.tick(FPS);
	
	pygame.quit();
if __name__ == "__main__":
	main();