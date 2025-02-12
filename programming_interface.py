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
            Block(50,50, 'forward')
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

<<<<<<< HEAD
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, font, text_color, action=None):
        """
        Below is a quick explanation for the pygame.Rect() button class, 
        param x: x position of the button
        param y: y position of the button
        param width: width of the button
        param height: height of the button
        param color: color of the button
        param hover_color: color of the button when hovered
        param text: text to display on the button
        param font: font of the text
        param text_color: color of the text
        param action: function to call when the button is clicked
=======
        for rect in self.blocks:
            rect.blit(self.screen)

        pygame.display.update()
        # pygame.display.flip()
>>>>>>> 502168ad32e8334dd7d95888bd3fac2a3d1fe2b7




class Block:
    def __init__(self, x, y, action):
        
        # Below is a quick explanation for the pygame.Rect() button class, 
        # param x: x position of the button
        # param y: y position of the button
        # param width: width of the button
        # param height: height of the button
        # param color: color of the button
        # param hover_color: color of the button when hovered
        # param text: text to display on the button
        # param font: font of the text
        # param text_color: color of the text
        # param action: function to call when the button is clicked
        color = (255,255,255)

        self.width, self.height = 100, 50

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Enables transparency
        self.surface.fill(color)  # Fill the rectangle with green

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
