import pygame
import pygame_gui
from sys import exit

# Pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("AM - Health star rating calculator")

UI_MANAGER = pygame_gui.UIManager((1280, 720))

FONTS = {
    "title": pygame.font.Font("freesansbold.ttf", 64),
    "text": pygame.font.Font("freesansbold.ttf", 32)
}

def draw_text(text="Text", pos=(0, 0), font=FONTS["text"], color=(255, 255, 255), surface=SCREEN):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = pos
    surface.blit(textobj, textrect)

def create_text_input_box(pos=(0, 0), dimentions=(200, 50), manager=UI_MANAGER, only_numbers=True):
    text_input_rect = pygame.Rect(pos, dimentions)
    text_input_box = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_rect, manager=manager)

    if only_numbers:
        text_input_box.set_allowed_characters("0123456789.")

    return text_input_box

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    UI_MANAGER.update(pygame.time.get_ticks())
    UI_MANAGER.draw_ui(SCREEN)

    pygame.display.update()

    SCREEN.fill((0, 0, 0))