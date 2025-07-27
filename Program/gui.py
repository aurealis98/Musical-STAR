import pygame
import pygame_textinput
import api
from sys import exit
from game import SCREEN_WIDTH, SCREEN_HEIGHT, DISPLAY, CLOCK, FRAMERATE
import game

pygame.init()
pygame.scrap.init()
pygame.display.set_caption("Musical STAR")
# FONTS
default_font = pygame.font.Font(None, 30)
joystix_font = pygame.font.Font(r"./resources/joystix monospace.otf", 30)
joystix_font_small = pygame.font.Font(r"./resources/joystix monospace.otf", 15)
joystix_font_title = pygame.font.Font(r"./resources/joystix monospace.otf", 65)


# FUNCTIONS
def draw_text(txt: str, font: pygame.font.Font, dest: tuple[int, int],
              color: str | tuple = 'black', antialias=False, screen=DISPLAY):
    text = font.render(txt, antialias, color)
    screen.blit(text, dest)


# CLASSES
class Button:
    def __init__(self, pos: tuple[int, int], dimensions: tuple[int, int], color: str | tuple,
                 outline_color: str | tuple = 'black', thickness: int = 0, screen=DISPLAY):
        self.text = ""
        self.pos = pos
        self.dimensions = dimensions    # (width, height)
        self.color = color
        self.outline_color = outline_color
        self.hover_color = 'gray'
        self.thickness = thickness
        self.screen = screen

        self.rect = pygame.Rect(self.pos, self.dimensions)

    def draw(self):
        """Draw the button body."""
        pygame.draw.rect(self.screen, self.color, self.rect)

        if self.thickness != 0:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, self.hover_color, self.rect, self.thickness)
            else:
                pygame.draw.rect(self.screen, self.outline_color, self.rect, self.thickness)

    def draw_text(self, txt: str, font: pygame.font.Font = default_font,
                  color: str | tuple = 'black', antialias=False, screen=DISPLAY):
        """Draw button text."""
        text = font.render(txt, antialias, color)

        # Centralize the text in button body
        textrect = text.get_rect()
        center = (self.rect.topleft[0] + self.dimensions[0]/2,
                  self.rect.topleft[1] + self.dimensions[1]/2)
        textrect.center = center

        screen.blit(text, textrect)

    @staticmethod
    def action(link: 'Screen'):
        """ If button is clicked, perform and action."""
        if isinstance(link, Screen):
            link.is_running()


class SearchBox:
    """
    Uses pygame-textbox to allow users to input an artist. Calls api functions to verify input as a valid artist.
    """

    def __init__(self, pos: tuple[int, int], dimensions: tuple[int, int], color: str | tuple = 'gray',
                 fontcolor: str | tuple = 'black', font: pygame.font.Font = default_font, screen=DISPLAY):
        self.screen = screen
        self.pos = pos
        self.dimensions = dimensions
        self.fontcolor = fontcolor
        self.color = color
        self.rect = pygame.Rect(self.pos, self.dimensions)

        self.text_input = pygame_textinput.TextInputVisualizer()
        self.text_input.font_object = font
        self.text_input.font_color = self.fontcolor
        self.terminated = False
        self.input_state = None
        self.found = ''

    def draw(self):
        """Draw search box body and information about user input."""
        pygame.draw.rect(self.screen, self.color, self.rect)

        if self.input_state is None:
            pass
        elif self.input_state == 0:
            draw_text("Empty", joystix_font_small,
                      (self.rect.bottomleft[0], self.rect.bottomleft[1] + 20),
                      'black')
        elif self.input_state == 2:
            draw_text(f"Closest artist match: {self.found[0]['name']}", joystix_font_small,
                      (self.rect.bottomleft[0], self.rect.bottomleft[1] + 20),
                      'black')
        elif self.input_state == 1:
            draw_text("Artist not found. Warning: Random results.", joystix_font_small,
                      (self.rect.bottomleft[0], self.rect.bottomleft[1] + 20),
                      'red')
        elif self.input_state == -1:
            draw_text("An error has occured.", joystix_font_small,
                      (self.rect.bottomleft[0], self.rect.bottomleft[1] + 20),
                      'red')

    def get_input(self, events_list: pygame.event.get()):
        """Draw and update input text."""
        if self.terminated is False:
            self.text_input.cursor_visible = True
            self.text_input.update(events_list)
        else:
            self.text_input.cursor_visible = False
        self.screen.blit(self.text_input.surface, (self.pos[0] + self.dimensions[0]/20,
                                                   self.pos[1] + self.dimensions[1]/4))

        return self.text_input.value

    def validate_input(self, artist: str):
        """Check if artist can be found or not with api call. Alter input state based on result."""
        if artist == '':
            self.input_state = 0
            return

        found = api.search_artist(artist)
        if found == 6:
            self.input_state = 1

        elif found == -1:
            self.input_state = -1

        else:
            self.input_state = 2
            self.found = found


class Screen:
    """Default screen template."""
    def __init__(self):
        self.running = False

    def is_running(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

            DISPLAY.fill('white')
            pygame.display.update()
            CLOCK.tick(FRAMERATE)


class MainMenu(Screen):
    """The first screen of the game=."""
    def __init__(self):
        super().__init__()
        self.running = False

    def is_running(self):
        self.running = True

        PlayButton = Button((250, 300), (100, 50), 'white', thickness=4)
        InfoButton = Button((230, 400), (140, 50), 'white', thickness=4)

        while self.running:
            DISPLAY.fill('white')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_coord = pygame.mouse.get_pos()
                        if PlayButton.rect.collidepoint(mouse_coord):
                            PlayButton.action(InputScreen())
                        if InfoButton.rect.collidepoint(mouse_coord):
                            InfoButton.action(InfoScreen())

            PlayButton.draw()
            InfoButton.draw()
            draw_text("MUSIC STAR", joystix_font_title, (40, 50))
            draw_text("A musical claw machine game", joystix_font_small, (145, 140))
            PlayButton.draw_text("PLAY", joystix_font_small, 'black')
            InfoButton.draw_text("GAME INFO", joystix_font_small, 'black')
            pygame.display.update()
            CLOCK.tick(FRAMERATE)


class InfoScreen(Screen):
    def __init__(self):
        super().__init__()
        self.running = False

    def is_running(self):
        self.running = True
        outer_box = pygame.Rect((25, 25), (SCREEN_WIDTH-50, SCREEN_HEIGHT-50))
        while self.running:
            DISPLAY.fill('white')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            pygame.draw.rect(DISPLAY, (180, 180, 180), outer_box, width=6)
            draw_text("CONTROLS", joystix_font, (200, 50))
            draw_text("Space - Move down and grab", joystix_font_small, (80, 140))
            draw_text("Q - Drop the prize", joystix_font_small, (80, 180))
            draw_text("E - Open the prize", joystix_font_small, (80, 220))
            draw_text("W or UP ARROW - Move up", joystix_font_small, (80, 300))
            draw_text("A or RIGHT ARROW - Move left", joystix_font_small, (80, 340))
            draw_text("S or DOWN ARROW - Move down", joystix_font_small, (80, 380))
            draw_text("D or RIGHT ARROW - Move right", joystix_font_small, (80, 420))
            pygame.display.update()
            CLOCK.tick(FRAMERATE)


class InputScreen(Screen):
    """Display search boxes which acquires input from user and checks it.
    It then sends input to variables in the prizes module.
    """

    def __init__(self):
        super().__init__()
        self.running = False

    @staticmethod
    def check_slots(slot_list: list):
        number = 3
        if slot_list[0] == '':
            number -= 1
        if slot_list[1] == '':
            number -= 1
        if slot_list[2] == '':
            number -= 1
        return number

    def is_running(self):
        self.running = True
        FirstBox = SearchBox((20, 100), (560, 80), font=joystix_font)
        SecondBox = SearchBox((20, 250), (560, 80), font=joystix_font)
        ThirdBox = SearchBox((20, 400), (560, 80), font=joystix_font)
        MaxNumberBox = SearchBox((520, 530), (50, 30), color=(230, 230, 230), font=joystix_font_small)

        SecondBox.terminated = True
        ThirdBox.terminated = True
        MaxNumberBox.terminated = True

        ProceedButton = Button((220, 600), (140, 50), 'white', thickness=4)
        proceed = False

        Elements = [FirstBox, SecondBox, ThirdBox, MaxNumberBox, ProceedButton]
        first_input = ''
        second_input = ''
        third_input = ''
        number_input = ''

        MAXIMUM_PRIZES = 30     # Hard maximum: 100
        SLOTS = ['', '', '']
        NUMBER_ENTERED = 0

        while self.running:
            DISPLAY.fill('white')
            eventslist = pygame.event.get()
            for event in eventslist:

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                # Clicking between search boxes
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_coords = pygame.mouse.get_pos()

                        if ProceedButton.rect.collidepoint(mouse_coords) and proceed is True:
                            ProceedButton.action(LoadingScreen(SLOTS, NUMBER_ENTERED, MAXIMUM_PRIZES))
                            break

                        elif MaxNumberBox.rect.collidepoint(mouse_coords):
                            MaxNumberBox.terminated = False
                            FirstBox.terminated = True
                            SecondBox.terminated = True
                            ThirdBox.terminated = True
                        elif FirstBox.rect.collidepoint(mouse_coords):
                            MaxNumberBox.terminated = True
                            FirstBox.terminated = False
                            SecondBox.terminated = True
                            ThirdBox.terminated = True
                            proceed = False
                        elif SecondBox.rect.collidepoint(mouse_coords):
                            MaxNumberBox.terminated = True
                            FirstBox.terminated = True
                            SecondBox.terminated = False
                            ThirdBox.terminated = True
                            proceed = False
                        elif ThirdBox.rect.collidepoint(mouse_coords):
                            MaxNumberBox.terminated = True
                            FirstBox.terminated = True
                            SecondBox.terminated = True
                            ThirdBox.terminated = False
                            proceed = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    if event.key == pygame.K_RETURN:
                        FirstBox.terminated = True
                        SecondBox.terminated = True
                        ThirdBox.terminated = True
                        FirstBox.validate_input(first_input)
                        SecondBox.validate_input(second_input)
                        ThirdBox.validate_input(third_input)

                        if FirstBox.input_state == 2:
                            SLOTS[0] = FirstBox.found[0]['name']
                        else:
                            SLOTS[0] = ''

                        if SecondBox.input_state == 2:
                            SLOTS[1] = SecondBox.found[0]['name']
                        else:
                            SLOTS[1] = ''

                        if ThirdBox.input_state == 2:
                            SLOTS[2] = ThirdBox.found[0]['name']
                        else:
                            SLOTS[2] = ''

                        MAXIMUM_PRIZES = int(number_input)
                        NUMBER_ENTERED = self.check_slots(SLOTS)
                        proceed = True

            for element in Elements:
                element.draw()

            first_input = FirstBox.get_input(eventslist)
            second_input = SecondBox.get_input(eventslist)
            third_input = ThirdBox.get_input(eventslist)
            number_input = MaxNumberBox.get_input(eventslist)

            if number_input == '':
                if MaxNumberBox.terminated is True:
                    draw_text("30", joystix_font_small,
                              (520, 535), 'black')
                number_input = '30'
            elif number_input != '' and number_input.isnumeric() is False:
                number_input = '30'
                draw_text("Invalid number", joystix_font_small,
                          (370, 585), 'red')
                draw_text("Default: 30", joystix_font_small,
                          (370, 605), 'red')
            elif int(number_input) > 100:
                number_input = '100'
                draw_text("Maximum is 100", joystix_font_small,
                          (370, 585), 'red')
            elif int(number_input) == 0:
                    draw_text("Are you sure?", joystix_font_small,
                          (370, 585), 'red')

            draw_text("Enter Artists", joystix_font,
                      (140, 20), 'black')
            draw_text("(Please spell correctly! It affects accuracy.)", joystix_font_small,
                      (25, 80), 'black')

            if (first_input == '' and second_input == '' and third_input == '') or proceed is False:
                ProceedButton.outline_color = 'gray'
                ProceedButton.draw_text('PROCEED', joystix_font_small, 'gray')
                draw_text("Press enter", joystix_font_small,
                          (220, 660), 'black')
            else:
                ProceedButton.outline_color = 'black'
                ProceedButton.draw_text('PROCEED', joystix_font_small, 'black')
                draw_text("Click to proceed.", joystix_font_small,
                          (200, 660), 'black')

            draw_text("Max prizes:", joystix_font_small,
                      (370, 535), 'black')

            pygame.display.update()
            CLOCK.tick(FRAMERATE)


class LoadingScreen(Screen):
    """Display while game module and api searching for artists and generating the prizes."""
    def __init__(self, slots: list, number_entered: int, max_prizes):
        super().__init__()
        self.running = False
        self.slots = slots
        self.number_entered = number_entered
        self.max_prizes = max_prizes

    def retrieve_artist(self):
        searched_list = []
        for artist in self.slots:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            if artist == '':
                pass
            else:
                searched_list += api.get_similar_arists(artist, self.max_prizes, self.number_entered)

        if len(searched_list) < self.max_prizes:
            searched_list += api.search_more_artists(searched_list, self.max_prizes)
        return searched_list

    def is_running(self):
        self.running = True
        DISPLAY.fill('white')
        draw_text("Loading...", joystix_font,
                  (180, 300), 'black')
        pygame.display.update()
        artists = self.retrieve_artist()

        game.PlayerSingle.empty()
        game.AllSprites.empty()
        game.CollisionObjects.empty()
        game.PrizeBalls.empty()

        Claw = game.ClawPlayer()
        prizes = game.generate_prizes(artists, Claw, self.max_prizes)
        GameScreen(Claw, prizes).is_running()


class GameScreen(Screen):
    """Main game loop."""
    def __init__(self, player: game.ClawPlayer, prizes_list: list):
        super().__init__()
        self.running = False
        self.player = player
        self.prizes_list = prizes_list

    def is_running(self):
        self.running = True
        while self.running:
            DISPLAY.fill('white')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    if event.key == pygame.K_e:
                        self.player.image = self.player.closed
                        self.player.adjust_image()
                        self.player.open_prize()
                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                        overlay.fill('black')
                        overlay.set_alpha(125)
                        DISPLAY.blit(overlay, (0, 0))
                        PrizeScreen(self.player.artist_data).is_running()

            game.AllSprites.update()
            game.AllSprites.draw(DISPLAY)
            pygame.display.update()
            CLOCK.tick(FRAMERATE)


class PrizeScreen(Screen):
    """Display after getting a prize."""
    def __init__(self, artist_data: dict):
        super().__init__()
        self.running = False
        self.artist_data = artist_data

    def is_running(self):
        self.running = True
        copied = False
        while self.running:
            CopyButton = Button((80, 225), (60, 30), 'white', 'black', thickness=4)
            OkButton = Button((270, 585), (60, 50), 'white', thickness=4)

            prize_window = pygame.Surface((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
            prize_window.fill('white')
            y_offset = 320
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_coords = pygame.mouse.get_pos()
                        if OkButton.rect.collidepoint(mouse_coords):
                            self.running = False
                        elif CopyButton.rect.collidepoint(mouse_coords):
                            copied = True
                            url_copy = self.artist_data['url']
                            pygame.scrap.put(pygame.SCRAP_TEXT, url_copy.encode('utf-8'))

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            DISPLAY.blit(prize_window, (50, 50))

            draw_text("YOU GOT", joystix_font_small, (80, 90))
            draw_text(self.artist_data['name'], joystix_font, (80, 110))
            draw_text("URL:", joystix_font_small, (80, 180))
            draw_text(self.artist_data['url'], joystix_font_small, (85, 200))

            draw_text("TOP TRACKS", joystix_font, (75, y_offset - 30))
            y_offset += 30
            for track in self.artist_data['top_tracks']:
                draw_text(track['name'], joystix_font_small, (80, y_offset))
                y_offset += 30

            draw_text("TOP ALBUMS", joystix_font, (75, y_offset))
            y_offset += 30
            for album in self.artist_data['top_albums']:
                y_offset += 30
                draw_text(album['name'], joystix_font_small, (80, y_offset))

            OkButton.draw()
            OkButton.draw_text("OK", joystix_font_small)
            CopyButton.draw()
            CopyButton.draw_text("COPY", joystix_font_small)

            if copied is True:
                draw_text("Copied to Clipboard", joystix_font_small, (200, 225))
            pygame.display.update()
            CLOCK.tick(FRAMERATE)
