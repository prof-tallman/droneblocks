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
         #Need to have an event handling loop here
         for event in pygame.event.get():
          if event.type == pygame.QUIT:
           self.running = False #to actually exit the loop
        self.draw()

        pygame.quit()


    def draw(self):
        self.screen.fill(self.background_color)

        pygame.draw.rect(self.screen, (100,100,0), pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()

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


        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.action = action
        self.hovered = False

    def draw(self, screen):
        # Some basic highlighting courtesy of the quarto project
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)

        # Pygame includes a font module (pygame.font) to help render text for labels
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    #The rect.collidepoint() method is used to check if a point is inside a rectangle, can use it for highlighting detection
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()  # Call the action function if the button was clicked


if __name__ == "__main__":
    interface = Interface()

    interface.run()
