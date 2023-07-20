import random
import pygame

from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.heart import Heart
from dino_runner.components.power_ups.shield import Shield


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300) #250
            self.randomic_choice = random.randint(0,2)
            if self.randomic_choice == 0:
                self.power_ups.append(Shield())
            elif self.randomic_choice == 1:
                self.power_ups.append(Hammer())
            elif self.randomic_choice == 2:
                self.power_ups.append(Heart())

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.character.dino_rect.colliderect(power_up.rect):
                if self.randomic_choice != 2:
                    power_up.start_time = pygame.time.get_ticks()
                    game.character.shield = True
                    game.character.has_power_up = True
                    game.character.type = power_up.type
                    game.character.power_up_time = power_up.start_time + (power_up.duration * 1000)
                    self.power_ups.remove(power_up)
                elif self.randomic_choice == 2:
                    if game.lifes < 3:
                        game.lifes += 1
                        self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
    
    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300) #250