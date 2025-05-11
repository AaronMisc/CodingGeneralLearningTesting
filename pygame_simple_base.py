import pygame
import pygame_gui
from sys import exit
from os.path import join

FONTS = {
    "title": pygame.font.Font("freesansbold.ttf", 64),
    "heading": pygame.font.Font("freesansbold.ttf", 48),
    "text": pygame.font.Font("freesans.ttf", 32)
}

COLORS = pygame.colordict.THECOLORS

class Window:
    def __init__(self, display_name = "Display", dimensions = (1280, 720)):
        pygame.init()
        self.display = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(display_name)
        self.background_color = (0, 0, 0)
        self.ui_manager  = pygame_gui.UIManager((1280, 720))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.ui_manager.update(pygame.time.get_ticks())
            self.ui_manager.draw_ui(self.display)

            pygame.display.update()

            self.display.fill(self.background_color)
    
class Button(pygame.sprite.Sprite):
    def __init__(self, x=10, y=120, w=200, h=75, 
                 text_padding=10,
                 heading_text="Button", heading_text_colour=COLORS["black"], heading_text_font=FONTS["heading"], 
                 body_text="Body text", body_text_offset=25, body_text_colour=COLORS["black"], body_text_font=FONTS["text"], 
                 button_colour=COLORS["blue2"], border_colour=COLORS["blue3"], hover_colour=COLORS["green3"], border_hover_colour=COLORS["green4"], border_width=3,
                 resize=True):
        super().__init__()

        self.image = pygame.Surface((w, h))  # Create the button surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.button_colour = button_colour
        self.hover_colour = hover_colour
        self.heading_text = heading_text
        self.heading_text_colour = heading_text_colour
        self.heading_text_font = heading_text_font
        self.body_text = body_text
        self.body_text_colour = body_text_colour
        self.body_text_font = body_text_font
        self.text_padding = text_padding
        self.body_text_offset = body_text_offset
        self.is_hovered = False  # Track hover state

        self.border_colour = border_colour
        self.border_hover_colour = border_hover_colour
        self.border_width = border_width
        self.resize = resize
    
    def update(self):
        """Update the button."""
        # Check if the mouse is hovering over the button
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        colour = self.hover_colour if self.is_hovered else self.button_colour
        border_colour = self.border_hover_colour if self.is_hovered else self.border_colour

        # Fill the button background colour
        self.image.fill(colour)

        # Draw the border around the button
        pygame.draw.rect(self.image, border_colour, self.image.get_rect(), self.border_width)

        # Draw text
        draw_text((self.text_padding, self.text_padding), self.heading_text, self.heading_text_colour, self.heading_text_font, surface=self.image)
        draw_text((self.text_padding, self.body_text_offset + self.text_padding), self.body_text, self.body_text_colour, self.body_text_font, surface=self.image)

    def is_clicked(self):
        """Check if the button is clicked."""
        if self.is_hovered and pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
            return True
        return False

def draw_text(pos, text="Text", colour=COLORS["white"], font=FONTS["text"], line_spacing=5, wrap_text=False, centred=False, surface=pygame.display.get_surface(), return_size=False):
    if wrap_text:
        text = text.replace(". ", ".\n")
    
    if not isinstance(pos, list):
        pos = list(pos)
    if centred:
        pos[0] -= font.size(text)[0] // 2

    lines = text.split("\n")
    for line in lines:
        text_surface = font.render(line, True, colour)
        text_rect = text_surface.get_rect(topleft=pos)
        surface.blit(text_surface, text_rect)
        pos[1] += text_surface.get_height() + line_spacing
         
    if return_size:
        return (text_surface.get_width(), ((text_surface.get_height() + line_spacing) * len(lines)))    

def create_text_input_box(pos=(0, 0), dimentions=(200, 50), manager=None, only_numbers=False):
    text_input_rect = pygame.Rect(pos, dimentions)
    text_input_box = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_rect, manager=manager)

    if only_numbers:
        text_input_box.set_allowed_characters("0123456789.")

    return text_input_box

# file_pre_path = ""
# try:
#     open(join("CODE-2025LearningMatplotlib", "data.csv"), "r")
# except:
#     file_pre_path = "CodingGeneralLearningTesting"

# def convert_filename(path:list):
#     if file_pre_path != "":
#         path.insert(0, file_pre_path)
#     return join(*path)