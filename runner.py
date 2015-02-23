import pygame, sys;
import random;

BLACK = (0, 0, 0);
WHITE = (255, 255, 255);
RED = (255, 0, 0);
GREEN = (0, 255, 0);
BLUE = (0, 0, 255);

screen_height = 200;
screen_width = 850;

class Obsticle(pygame.sprite.Sprite):
    passed = False;
    def __init__(self, x, t):
        pygame.sprite.Sprite.__init__(self);
        if t == 1:
            self.image = pygame.Surface([15, 20]);
        elif t == 2:
            self.image = pygame.Surface([20, 20]);
        else:
            self.image = pygame.Surface([30, 20]);
        self.image.fill(RED);

        self.rect = self.image.get_rect();
        self.rect.y = screen_height - 20;
        self.rect.x = x;
    def move(self, x):
        self.rect.x -= x;
class view():
    delt_x = 4;
    tt = 0;
    def __init__(self):
        self.obs = pygame.sprite.Group()
    def init(self):
        self.obs.empty();

    def generate(self):
        t = random.randint(1,3);
        self.tt += 1;
        generate = random.randint(0, 30)
        if self.tt >= 30 and generate == 30:
            self.tt = 0;
            obs = Obsticle(screen_width + 26, t);
            self.obs.add(obs);
        return self.obs;
    def scroll(self, p):
        for i in self.obs:
            i.move(self.delt_x);
            if i.rect.right < 0:
                self.obs.remove(i);
            if i.rect.right < p.rect.left and not i.passed:
                i.passed = True;

class player(pygame.sprite.Sprite):
    delt_x = 0;
    delt_y = 0;
    score = 0;
    tt = 0;
    def __init__(self):
        pygame.sprite.Sprite.__init__(self);

        self.image = pygame.Surface([10,10]);
        self.image.fill(WHITE);
        self.rect = self.image.get_rect();
        self.rect.y = screen_height - 10;
        self.rect.x = 100;
        self.jumping = False;
    def init(self):
        self.delt_x = 0;
        self.delt_y = 0;
        self.score = 0;
        self.rect.y = screen_height - 10;
        self.jumping = False;
    def jump(self):
        if self.jumping: return;
        self.delt_y = 11;
        self.jumping = True;
    def move(self, obs):
        if self.rect.y >= screen_height - 9:
            self.rect.y = screen_height - 10;
            self.delt_y = 0;
            self.jumping = False;
        elif self.jumping:
            self.rect.y -= self.delt_y;
            self.delt_y -= 1;
        self.rect.x += self.delt_x;

        hit = pygame.sprite.spritecollide(self, obs, False);

        self.tt += 1;

        if self.tt > 10:
            self.addscore();
            self.tt = 0;
        return hit;
    def addscore(self):
        self.score += 1;
        print("score: ", self.score);
def main():
    pygame.init();

    fpsClock = pygame.time.Clock();
    FPS = 60;

    window = pygame.display.set_mode([screen_width, screen_height]);

    all_sprite_list = pygame.sprite.Group();
    v = view();
    obs = v.generate();

    p = player();
    all_sprite_list.add(p);

    done = False;
    gameover = False;
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True;
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    p.jump();
                    if gameover:
                        p.init();
                        v.init();

                        gameover = False;
        if not gameover:
            v.generate();
            gameover = p.move(obs);
            v.scroll(p);

        window.fill(BLACK);

        obs.draw(window);
        all_sprite_list.draw(window);

        pygame.display.flip();
        fpsClock.tick(FPS);

if __name__ == "__main__": main();
