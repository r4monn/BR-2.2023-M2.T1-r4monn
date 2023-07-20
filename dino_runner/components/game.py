import pygame

from dino_runner.utils.constants import BG, GAME_OVER, HEART, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "inkfree.ttf"
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.lifes = 3
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.character = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def show_text(self, text, pos_x, pos_y, color = "black"):
        font = pygame.font.Font(FONT_STYLE, 22) 
        text = font.render(text, True, (0, 0, 0)) if color == "black" else font.render(text, True, (255, 0, 0))  # noqa: E501
        text_rect = text.get_rect()
        if color == "red":
            font.set_bold(True) 

        if (pos_y is None) and (pos_x is None):
            text_rect.center = (HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)
        else:
            text_rect.center = (pos_x, pos_y)
        self.screen.blit(text, text_rect)

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        pygame.mixer.music.play(-1)
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.character.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 3

        self.totalScore = self.score

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.character.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_score()
        self.draw_lifes()
        self.draw_power_up_time()
        self.draw_deaths()
        pygame.display.update() # Desenhar os objetos na tela
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.show_text(f"Score: {self.score}", 1000, 50)

    def draw_power_up_time(self):
        if self.character.has_power_up:
            time_to_show = round((self.character.power_up_time - pygame.time.get_ticks()) / 1000, 1)  # noqa: E501
            if time_to_show >= 0:
                self.show_text(f"{self.character.type.capitalize()} enabled for {time_to_show} seconds", HALF_SCREEN_WIDTH, 50)  # noqa: E501
            else:
                self.character.has_power_up = False
                self.character.type = DEFAULT_TYPE

    def update_death_count(self):
        self.death_count += 1
    
    def draw_deaths(self):
        self.show_text(f"Deaths: {self.death_count}", 90, 80)

    def draw_lifes(self):
        if self.lifes == 1:
            self.screen.blit(HEART, (50, 35))
        elif self.lifes == 2:
            self.screen.blit(HEART, (50, 35))
            self.screen.blit(HEART, (70, 35))
        elif self.lifes == 3:
            self.screen.blit(HEART, (50, 35))
            self.screen.blit(HEART, (70, 35))
            self.screen.blit(HEART, (90, 35))
        # self.show_text(f"Lifes: {self.lifes}", 200, 50)

    def show_menu(self):
        self.screen.fill((255, 255, 255))

        if self.death_count == 0:
            self.show_text("Press any key to start", None, None)
        else: ## tela de restart
            self.screen.blit(GAME_OVER, (HALF_SCREEN_WIDTH - 200, 80))
            self.show_text("You died", HALF_SCREEN_WIDTH, 130, "red")
            self.show_text(f"Score: {self.totalScore}", HALF_SCREEN_WIDTH, 160)
            self.screen.blit(ICON, (HALF_SCREEN_WIDTH - 40, HALF_SCREEN_HEIGHT - 110))
            self.show_text("Press any key to restart", HALF_SCREEN_WIDTH, 320)
            self.game_speed = 20
            self.score = 0
            ## mostrar mensagem de "Press any key to restart"   check
            ## mostrar o score atingido   check
            ## mostrar death_count  check

            ### Resetar score e game_speed quando uma nova partida for iniciada   check
            ### Criar método para remover a repetição de código para o texto   check
        pygame.display.update()
        self.handle_events_on_menu()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
                self.lifes = 3