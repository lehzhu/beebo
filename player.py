# player.py

import pygame

class Player:
    def __init__(self, image_path, start_pos, cell_size):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.angle = 0
        self.pos = start_pos

    def move(self, direction):
        # Handle movement and set angle based on direction
        # Update self.pos and self.angle accordingly

    def render(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        screen.blit(rotated_image, (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE))
