import pygame
import api
from random import randint
from sys import exit

pygame.init()
# PROGRAM VARIABLES
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
FRAMERATE = 60

# SPRITE LIST
PrizeBalls = pygame.sprite.Group()
PlayerSingle = pygame.sprite.GroupSingle()
CollisionObjects= pygame.sprite.Group()
AllSprites = pygame.sprite.Group()


# IMAGES
prizeball_red = pygame.image.load('./resources/prizeball_red.png').convert_alpha(DISPLAY)
prizeball_red = pygame.transform.smoothscale(prizeball_red, (80, 70))
prizeball_blue = pygame.image.load('./resources/prizeball_blue.png').convert_alpha(DISPLAY)
prizeball_blue = pygame.transform.smoothscale(prizeball_blue, (80, 70))
prizeball_pink = pygame.image.load('./resources/prizeball_pink.png').convert_alpha(DISPLAY)
prizeball_pink = pygame.transform.smoothscale(prizeball_pink, (80, 70))
prizeball_green = pygame.image.load('./resources/prizeball_green.png').convert_alpha(DISPLAY)
prizeball_green = pygame.transform.smoothscale(prizeball_green, (80, 70))
prizeball_yellow = pygame.image.load('./resources/prizeball_yellow.png').convert_alpha(DISPLAY)
prizeball_yellow = pygame.transform.smoothscale(prizeball_yellow, (80, 70))

claw_open = pygame.image.load('./resources/claw_open_long.png').convert_alpha(DISPLAY)
claw_open = pygame.transform.smoothscale(claw_open,(485, 890))
claw_closed = pygame.image.load('./resources/claw_closed_long.png').convert_alpha(DISPLAY)
claw_closed = pygame.transform.smoothscale(claw_closed, (200, 910))


class ClawPlayer(pygame.sprite.Sprite):
    def __init__(self, self_group=(PlayerSingle, AllSprites), collide_with=CollisionObjects):
        super().__init__(self_group)
        self.open = claw_open
        self.closed = claw_closed
        self.image = claw_closed

        self.x = SCREEN_WIDTH/2
        self.y = -1000
        self.width = 100
        self.height = 500

        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.claw_body_rect = pygame.Rect(self.rect.bottomleft, (50, 50))
        self.grab_rect = pygame.Rect(self.rect.bottomleft, (50, 50))

        self.collide_with = collide_with
        self.is_grabbing = False
        self.is_holding_FLAG = False
        self.grabbed_object = None
        self.artist_data = None

    def adjust_image(self):
        if self.image == self.open:
            self.rect = pygame.Rect((self.x - 135, self.y + 300), (self.width, self.height))
            self.claw_body_rect = pygame.Rect((self.rect.bottomleft[0] + 140, self.rect.bottomleft[1] + 330), (200, 30))
            self.grab_rect = pygame.Rect((self.rect.bottomleft[0] + 218, self.rect.bottomleft[1] + 350), (50, 20))

        elif self.image == self.closed:
            self.claw_body_rect = pygame.Rect((self.rect.bottomleft[0] + 80, self.rect.bottomleft[1] + 250), (55, 105))
            self.grab_rect = pygame.Rect((self.rect.bottomleft[0] + 69, self.rect.bottomleft[1] + 330), (80, 70))
            self.rect = pygame.Rect((self.x, self.y + 300), (self.width, self.height))

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            if self.is_holding_FLAG is True:
                pass
            else:
                self.image = self.open
                if self.y < -530:
                    self.y += 7
                self.grab()

        elif key[pygame.K_q]:
            self.image = self.open
            self.drop_prize()
        else:
            if self.y > -920:
                self.y -= 8
            self.image = self.closed

        #if key[pygame.K_e]:
            #self.image = self.closed
            #self.open_prize()

        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and not key[pygame.K_SPACE] and self.x < SCREEN_WIDTH - 100:
            self.x += 5
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and not key[pygame.K_SPACE] and self.x > -100:
            self.x -= 5
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.y < -750:
            self.y += 5
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.y > -1050:
            self.y -= 5

        self.adjust_image()

    def grab(self):
        prizeballs = list(self.collide_with)
        collided = self.grab_rect.collidelist(prizeballs)

        if collided != -1 and self.is_holding_FLAG is False and \
        prizeballs[collided].is_grabbed_FLAG is False:

            self.is_holding_FLAG = True
            self.grabbed_object = prizeballs[collided]
            self.grabbed_object.is_grabbed_FLAG = True

    def open_prize(self):
        prizeballs = list(self.collide_with)
        collided = self.grab_rect.collidelist(prizeballs)

        if collided != -1 and self.is_holding_FLAG is True and \
                prizeballs[collided].is_grabbed_FLAG is True:
            toptracks = list(api.get_top_tracks(self.grabbed_object.artist))
            topalbums = list(api.get_top_albums(self.grabbed_object.artist))
            self.artist_data = {'name': self.grabbed_object.artist, 'url': self.grabbed_object.artist_link,
                           'top_tracks': toptracks[:3], 'top_albums': topalbums[:3]}

            self.grabbed_object.kill()
            self.is_holding_FLAG = False
            self.grabbed_object.is_grabbed_FLAG = False
            self.grabbed_object = None

    def drop_prize(self):
        prizeballs = list(self.collide_with)
        collided = self.grab_rect.collidelist(prizeballs)

        if collided != -1 and self.is_holding_FLAG is True and \
        prizeballs[collided].is_grabbed_FLAG is True:
            self.is_holding_FLAG = False
            self.grabbed_object.is_grabbed_FLAG = False
            self.grabbed_object = None


class PrizeBall(pygame.sprite.Sprite):
    def __init__(self, x, y, player: ClawPlayer, self_group=(PrizeBalls, CollisionObjects, AllSprites),
                 collide_with=CollisionObjects):
        super().__init__(self_group)
        self.image = self.choose_ball()
        self.image_core = pygame.transform.scale(self.image, (30, 30))

        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2()

        self.rect = self.image_core.get_rect(center=self.position)
        self.old_rect = self.rect.copy()

        self.artist = None
        self.artist_link = None
        self.top_tracks = None
        self.top_albums = None
        self.collide_with = collide_with
        self.player = player
        self.is_grabbed_FLAG = False

    @staticmethod
    def choose_ball():
        prizeballs = [prizeball_red, prizeball_yellow, prizeball_green, prizeball_blue, prizeball_pink]
        index = randint(0, 4)
        return prizeballs[index]

    def set_is_grabbed_FLAG(self, boolean: bool, player: ClawPlayer):
        self.is_grabbed_FLAG = boolean
        self.player = player

    def collision(self, direction: str):
        for ball in pygame.sprite.spritecollide(self, self.collide_with, False):
            if ball is self:
                continue
            if direction == 'horizontal' and self.rect.colliderect(ball.rect):
                # Collision on Right (Other object collides its left)
                if self.rect.right >= ball.rect.left and self.old_rect.right <= ball.old_rect.left:
                    self.rect.right = ball.rect.left
                    self.position.x = ball.rect.x

                # Collision on Left (Other object collides its right)
                if self.rect.left <= ball.rect.right and self.old_rect.left >= ball.old_rect.right:
                    self.rect.left = ball.rect.right
                    self.position.x = ball.rect.x

            if direction == 'vertical' and self.rect.colliderect(ball.rect):

                # Collision on Bottom (Other object collides its top)
                if self.rect.bottom >= ball.rect.top and self.old_rect.bottom <= ball.old_rect.top:
                    self.rect.bottom = ball.rect.top
                    self.position.y = ball.rect.y

                # Collision on Top (Other object collides its bottom)
                if self.rect.top <= ball.rect.bottom and self.old_rect.top >= ball.old_rect.bottom:
                    self.rect.top = ball.rect.bottom
                    self.position.y = ball.rect.y

    def border_collision(self):
        if self.rect.bottom < SCREEN_HEIGHT - 50:
            self.position.y += 5
            self.rect.bottom += 5
        if self.rect.bottom > SCREEN_HEIGHT - 40:
            self.position.y = SCREEN_HEIGHT - 100
            self.rect.bottom = SCREEN_HEIGHT - 100

        if self.rect.right >= SCREEN_WIDTH - 20:
            self.position.x = randint(50, SCREEN_WIDTH - 40)
            self.rect.right = randint(50, SCREEN_WIDTH - 40)
            self.position.y = randint(100, SCREEN_HEIGHT - 300)
            self.rect.bottom = randint(100, SCREEN_HEIGHT - 300)

        if self.rect.left <= 20:
            self.position.x = randint(50, SCREEN_WIDTH - 40)
            self.rect.right = randint(50, SCREEN_WIDTH - 40)
            self.position.y = randint(100, SCREEN_HEIGHT - 300)
            self.rect.bottom = randint(100, SCREEN_HEIGHT - 300)

    def update(self):
        self.old_rect = self.rect.copy()
        self.border_collision()
        self.collision('horizontal')
        self.collision('vertical')
        if self.is_grabbed_FLAG is True and self.player.is_holding_FLAG is True:
            if self.player.image == self.player.closed:
                self.rect.center = (self.player.grab_rect.center[0] - 22,
                                   self.player.grab_rect.center[1] - 25)


def generate_prizes(artist_list: list, player: ClawPlayer, max_prizes):
    """Use methods from the api to generate prizes and embed them with the artist."""
    prizes_list = []
    if len(artist_list) != 0:
        for i in range(max_prizes):
            prize = PrizeBall(randint(70, SCREEN_WIDTH - 70), randint(100, SCREEN_HEIGHT), player)
            prize.artist = artist_list[i]['name']
            prize.artist_link = artist_list[i].get('url')
            prizes_list.append(prize)
    return prizes_list