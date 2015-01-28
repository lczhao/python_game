import pygame, sys;
import random;

BLACK = (0, 0, 0);
WHITE = (255, 255, 255);
RED = (255, 0, 0);
GREEN = (0, 255, 0);
BLUE = (0, 0, 255);

class Wall(pygame.sprite.Sprite):
	def __init__(self, color, x, y, width, height):
		pygame.sprite.Sprite.__init__(self);	#parent constructor;
		
		self.image = pygame.Surface([width, height]);
		self.image.fill(color);
		
		self.rect = self.image.get_rect();
		self.rect.y = y;
		self.rect.x = x;

		
class Player(pygame.sprite.Sprite):
	deltX = 0;
	deltY = 0;
	
	def __init__ (self, x, y):
		super().__init__();
		
		self.image = pygame.Surface([15, 15]);
		self.image.fill(WHITE);
		
		self.rect = self.image.get_rect();
		
		self.rect.y = y;
		self.rect.x = x;
	
	def change_speed (self, x, y):
		self.deltX += x;
		self.deltY += y;
	
	def move (self, walls):
	
		self.rect.x += self.deltX;
		
		block_hit = pygame.sprite.spritecollide(self, walls, False);
		for block in block_hit:
			#moving to left
			if self.deltX > 0:
				self.rect.right = block.rect.left;
			else:
				self.rect.left = block.rect.right;
		
		self.rect.y += self.deltY;
		
		block_hit = pygame.sprite.spritecollide(self, walls, False);
		for block in block_hit:
			
			if self.deltY > 0:
				self.rect.bottom = block.rect.top;
			else:
				self.rect.top = block.rect.bottom;
				
class Room():
	wall_list = None; 		#empty to start with
	enemy_sprites = None;
	
	def __init__(self):
		self.wall_list = pygame.sprite.Group();
		self.enemy_sprites = pygame.sprite.Group();

wall_width = 20;
door_height = 100;
window_height = 550;
window_width = 500;

class Room1(Room):
	
	def __init__(self):
		super().__init__();
		
		walls = [
			[BLUE, 0, 0, wall_width, int(window_height / 2 - door_height/2)],			#Left Door
			[BLUE, 0, int(window_height / 2 + door_height/2), wall_width, int(window_height / 2 - door_height/2)],
			[BLUE, 0, 0, window_width, wall_width],			#Upper Border
			[BLUE, 0, 530, window_width, wall_width],		#Lower Border
			[BLUE, window_width - wall_width, 0, wall_width, int(window_height / 2 - door_height/2)],
			[BLUE, window_width - wall_width, int(window_height / 2 + door_height/2) , wall_width, int(window_height / 2 - door_height/2)],
			[WHITE, 400, 50, 20, 450],
			[WHITE, 250, 50, 20, 450],
			[WHITE, 100, 50, 20, 450]
		];
		
		for wall in walls:
			# Wall(color, x, y, width, height);
			w = Wall(wall[0], wall[1], wall[2], wall[3], wall[4]);
			self.wall_list.add(w);
			
class Room2(Room):
	
	def __init__(self):
		super().__init__();
		
		walls = [
			[	
				RED, 0, 0, 
				wall_width, 
				int(window_height / 2 - door_height/2)
			],			#Left Door
			[
				RED, 0, int(window_height / 2 + door_height/2), 
				wall_width, 
				int(window_height / 2 - door_height/2)
			],
			[RED, 0, 0, window_width, wall_width],			#Upper Border
			[RED, 0, 530, window_width, wall_width],		#Lower Border
			[RED, window_width - wall_width, 0, wall_width, int(window_height / 2 - door_height/2)],
			[RED, window_width - wall_width, int(window_height / 2 + door_height/2) , wall_width, int(window_height / 2 - door_height/2)],
			[WHITE, 50, 50, 400, 20],
			[WHITE, 50, 150, 400, 20],
			[WHITE, 50, 250, 400, 20]
		];
		
		for wall in walls:
			# Wall(color, x, y, width, height);
			w = Wall(wall[0], wall[1], wall[2], wall[3], wall[4]);
			self.wall_list.add(w);

def main():
	pygame.init();
	
	FPS = 60;
	fpsClock = pygame.time.Clock();
	
	window = pygame.display.set_mode([window_width, window_height]);
	
	#Initialize the player here..
	player = Player(0, 275);
	movingsprites = pygame.sprite.Group();
	movingsprites.add(player);
	
	#Initialize the room here
	rooms = [];

	room = Room1();
	rooms.append(room);

	room = Room2();
	rooms.append(room);

	current_room_no = 0;
	current_room = rooms[current_room_no];
	
	done = False;
	
	# Event loops
	while not done:
	
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				done = True
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					
					player.change_speed(-5, 0)
				if event.key == pygame.K_RIGHT:
					player.change_speed(5, 0)
				if event.key == pygame.K_UP:
					player.change_speed(0, -5)
				if event.key == pygame.K_DOWN:
					player.change_speed(0, 5)
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					player.change_speed(5, 0)
				if event.key == pygame.K_RIGHT:
					player.change_speed(-5, 0)
				if event.key == pygame.K_UP:
					player.change_speed(0, 5)
				if event.key == pygame.K_DOWN:
					player.change_speed(0, -5)
		
		#Game calculation ...
		player.move(current_room.wall_list);
		
		#Logic
		if player.rect.x < -15:
			current_room_no = (current_room_no - 1) % len(rooms);
			current_room = rooms[current_room_no];
			player.rect.x = window_width - 15;
		elif player.rect.x > window_width + 1:
			current_room_no = (current_room_no + 1) % len(rooms);
			current_room = rooms[current_room_no];
			player.rect.x = 0;
		
		#Redraw every thig here ..
		window.fill(BLACK);
		
		movingsprites.draw(window);
		current_room.wall_list.draw(window);
		
		pygame.display.flip();
		
		fpsClock.tick(FPS);
		
if __name__ == "__main__":
	main();