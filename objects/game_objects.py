# find all the Game objects in here
import pygame


class Player:

    def __init__(self, x, y, width, height, color):
        self.x = x  # defines position on x-axis
        self.y = y  # defines position on y-axis
        self.width = width
        self.heigth = height
        self.color = color  # defines the color of the player rectangle
        self.rect = (x, y, width, height)  # defines the rectangle as player object defined height*width
        self.vel = 3    # defines the speed of the object when pressing key

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):

        # returns a list of keys and if they are pressed the value will be a one
        keys = pygame.keys.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y += self.vel

        if keys[pygame.K_DOWN]:
            self.y -= self.vel

        # update the player position
        self.rect(self.x, self.y, self.width, self.heigth)




