# Importing the library
import pygame
 
 
class Interface:
    def __init__(self):
        # Initializing Pygame
        pygame.init()
        self.running = True

        self.SIZE = (900, 700)
        self.screen = pygame.display.set_mode(self.SIZE)
        self.background_color = (0, 0, 50)


    def run(self):
        while self.running:
            self.draw()

        pygame.quit()


    def draw(self):
        self.screen.fill(self.background_color)

        pygame.draw.rect(self.screen, (100,100,0), pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()

if __name__ == "__main__":
    interface = Interface()

    interface.run()