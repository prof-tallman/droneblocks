# Importing the library
import pygame
 
 
class Interface:
    def __init__(self):
        # Initializing Pygame
        pygame.init()
        self.running = True

        self.SIZE = (1280, 720)
        self.screen = pygame.display.set_mode(self.SIZE)
        self.background_color = (0, 0, 50)
        
        self.blocks = [
            Block(50, 300, 'rotate_ccw'),
            Block(150, 300, 'forward'),
            Block(250, 300, 'rotate_cw'),
            Block(50, 400, 'left'),
            Block(150, 400, 'backward'),
            Block(250, 400, 'right'),
            Block(50, 500, 'up'),
            Block(150, 500, 'hover'),
            Block(250, 500, 'down'),
            Block(100, 600, 'takeoff'),
            Block(200, 600, 'land')
        ]

    def run(self):
        while self.running:
            #Need to have an event handling loop here
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("MOUSE CLICKED")

                if event.type == pygame.QUIT:
                    self.running = False #to actually exit the loop



            self.draw()

        pygame.quit()


    def draw(self):
        self.screen.fill(self.background_color)

        # text_surface = self.font.render(self.text, True, self.text_color)
        # text_rect = text_surface.get_rect(center=self.rect.center)

        for rect in self.blocks:
            rect.blit(self.screen)

        pygame.display.update()
        # pygame.display.flip()


class Block:
    def __init__(self, x: int, y: int, action: str):
        """
        Initializes a new pygame rectangle object.
        
        Parameters:
            x (int): The x-coordinate of the object's position.
            y (int): The y-coordinate of the object's position.
            action (str): The text to be displayed on the object.
        """
        color = (255,255,255)

        self.width, self.height = 75, 75

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Enables transparency
        self.surface.fill(color)  # Fill the rectangle with green

        temp_font = pygame.font.SysFont('Arial', 14).render(action, True, (0, 0, 0))
        self.surface.blit(temp_font, (5, 5))

        self.action = action

        self.x = x
        self.y = y


    def blit(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    #The rect.collidepoint() method is used to check if a point is inside a rectangle, can use it for highlighting detection
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            print(f"{self.action} clicked")
            self.action()  # Call the action function if the button was clicked


if __name__ == "__main__":
    interface = Interface()

    interface.run()
