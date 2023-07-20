import pygame
import random

from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, SMALL_CACTUS, LARGE_CACTUS


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        
    def update(self, game):
        if len(self.obstacles) == 0:
            obstacleType = random.randint(0, 3)
            if obstacleType == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif obstacleType == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            else:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.character.dino_rect.colliderect(obstacle):
                if not game.character.has_power_up and game.lifes > 1:
                    game.lifes -= 1
                    self.obstacles.remove(obstacle)
                elif not game.character.has_power_up and game.lifes <= 1:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
