import pygame
import pygame_gui
from sys import exit

# Pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("AM - Health star rating calculator")

UI_MANAGER = pygame_gui.UIManager((1280, 720))

fonts = {
    "title": pygame.font.Font("freesansbold.ttf", 64),
    "text": pygame.font.Font("freesansbold.ttf", 32)
}

def draw_text(text="Text", pos=(0, 0), font=fonts["text"], color=(255, 255, 255), surface=SCREEN):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = pos
    surface.blit(textobj, textrect)

def energy_points(E):
    return -((1 / 335) * (E - 2345) + 7) if E != 0 else 0

def saturated_fat_points(S):
    return -((1 / 1.4) * (S - 9) + 9) if S != 0 else 0

def total_sugars_points(S):
    answer = -((1 / 3.9) * (S - 5) + 0)
    return answer if answer < 0 else 0

def sodium_points(Na):
    answer = -((1 / 90) * (Na - 90) + 0) if Na != 0 else 0
    return answer if answer < 0 else 0

def fvnl_points(FVNL):
    answer = (4 / 25) * (FVNL - 75) + 4
    return answer if answer > 0 else 0

def fibre_points(F):
    return (1 / 1.8) * (F - 11.2) + 11 if F != 0 else 0

def protein_points(P):
    return (1 / 6.7) * (P - 24) + 11 if P != 0 else 0

def food_rating(T):
    return -0.114286 * T + 3.35714 if T != 0 else 0

def create_text_input_box(pos=(0, 0), dimentions=(200, 50), manager=UI_MANAGER, only_numbers=True):
    text_input_rect = pygame.Rect(pos, dimentions)
    text_input_box = pygame_gui.elements.UITextEntryLine(relative_rect=text_input_rect, manager=manager)

    if only_numbers:
        text_input_box.set_allowed_characters("0123456789.")

    return text_input_box

def create_buttom(pos=(0, 0), dimentions=(200, 50), manager=UI_MANAGER, text="Button"):
    button_rect = pygame.Rect(pos, dimentions)
    button = pygame_gui.elements.UIButton(relative_rect=button_rect, text=text, manager=manager)

    return button

food_input_names = ["Energy", "Saturated Fat", "Total Sugars", "Sodium", "FVNL", "Fibre", "Protein"]
health_food_names = ["FVNL", "Fibre", "Protein"]

food_input_name_function = {
    "Energy": energy_points,
    "Saturated Fat": saturated_fat_points,
    "Total Sugars": total_sugars_points,
    "Sodium": sodium_points,
    "FVNL": fvnl_points,
    "Fibre": fibre_points,
    "Protein": protein_points
}

food_input_boxes = {}
for i, food_input_name in enumerate(food_input_names):
    food_input_boxes[food_input_name] = create_text_input_box(pos=(400, 100+i*50), dimentions=(200, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.VIDEORESIZE:
            SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            UI_MANAGER.set_window_resolution((event.w, event.h))
        
        UI_MANAGER.process_events(event)
    
    draw_text("Health star rating calculator", (20, 20), font=fonts["title"])
    draw_text("Project made by AaronMisc.\nThis is for fun, not accurate.", (20, 550), font=fonts["title"], color=(200, 80, 0))

    for food_input_name, food_input_box in food_input_boxes.items():
        draw_text(f"{food_input_name}", (20, food_input_box.relative_rect.y), font=fonts["text"], color=(0, 200, 0) if food_input_name in health_food_names else (200, 0, 0))

        try:
            text = food_input_name_function[food_input_name](float(food_input_box.get_text()))
        except:
            text = "Error"

        draw_text(f"Points: {text}", (700, food_input_box.relative_rect.y), font=fonts["text"])

    draw_text("All", (20, 510), font=fonts["text"])

    try:
        text = sum([food_input_name_function[food_input_name](float(food_input_box.get_text())) for food_input_name, food_input_box in food_input_boxes.items()])
    except:
        text = "Error"

    draw_text(f"Total: {text}", (400, 460), font=fonts["text"])
    
    try:
        text = food_rating(sum([food_input_name_function[food_input_name](float(food_input_box.get_text())) for food_input_name, food_input_box in food_input_boxes.items()]))
    except:
        text = "Error"

    draw_text(f"Final rating: {text}/5", (400, 510), font=fonts["text"])

    UI_MANAGER.update(pygame.time.get_ticks())
    UI_MANAGER.draw_ui(SCREEN)

    pygame.display.update()

    SCREEN.fill((0, 0, 0))