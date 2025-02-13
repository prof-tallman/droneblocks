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
            Block(25, 200, 'rotate_ccw'),
            Block(150, 200, 'forward'),
            Block(275, 200, 'rotate_cw'),
            Block(25, 325, 'left'),
            Block(150, 325, 'backward'),
            Block(275, 325, 'right'),
            Block(25, 450, 'up'),
            Block(150, 450, 'hover'),
            Block(275, 450, 'down'),
            Block(87.5, 575, 'takeoff'),
            Block(212.5, 575, 'land')
        ]

    def run(self):
        while self.running:
            #Need to have an event handling loop here
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for block in self.blocks:
                        if block.surface_rectangle.collidepoint(event.pos):
                            block.dragging = True
                            print(block.dragging)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for block in self.blocks:
                        if block.surface_rectangle.collidepoint(event.pos):
                            block.dragging = False
                            print(block.dragging)
                elif event.type == pygame.MOUSEMOTION:
                    for block in self.blocks:
                        if block.dragging:
                            if block.surface_rectangle.collidepoint(event.pos):
                                mouse_x, mouse_y = event.pos
                                block.x = mouse_x - block.width // 2
                                block.y = mouse_y - block.height // 2
                                block.surface_rectangle.topleft = (block.x, block.y)
                                print(block.x, block.y)

                if event.type == pygame.QUIT:
                    self.running = False #to actually exit the loop



            self.draw()

        pygame.quit()


    def draw(self):
        self.screen.fill(self.background_color)

        # text_surface = self.font.render(self.text, True, self.text_color)
        # text_rect = text_surface.get_rect(center=self.rect.center)

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(400, 0, 1, self.SIZE[1])) # divider between blocks and control area

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
        
        self.x = x
        self.y = y
        self.width, self.height = 100, 100
        self.action = action
        self.dragging = False

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Enables transparency
        self.surface.fill((200, 200, 200))
        
        self.surface_rectangle = self.surface.get_rect() # drawing rectangle exactly to the surface to enable interactivity like collidepoint
        self.surface_rectangle.topleft = (self.x, self.y) 

    def blit(self, screen: pygame.Surface):
        screen.blit(self.surface, (self.x, self.y))
        
        self.check_hover(pygame.mouse.get_pos())
        # self.check_click(pygame.mouse.get_pos())

        # temporary font so that we can see the names of the blocks
        temp_font = pygame.font.SysFont('Arial', 14).render(self.action, True, (0, 0, 0))
        self.surface.blit(temp_font, (5, 5))

    #The rect.collidepoint() method is used to check if a point is inside a rectangle, can use it for highlighting detection
    def check_hover(self, mouse_pos):
        if self.surface_rectangle.collidepoint(mouse_pos):
            self.surface.fill((200, 200, 200))
        else:
            self.surface.fill((255, 255, 255))

    def check_click(self, mouse_pos):
        if self.surface_rectangle.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            print(f"{self.action} clicked")
            


if __name__ == "__main__":
    interface = Interface()

    interface.run()
