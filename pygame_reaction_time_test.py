import pygame
import statistics
from sys import exit
from random import randint

copying_enabled = True # Change to False if you don't want to use pyperclip
if copying_enabled: from pyperclip import copy

pygame.init()
COLORS = pygame.colordict.THECOLORS
SETTINGS = {
    "Video": {
        "Normal text size": 18, # In pixels
        "Large text size": 48, # In pixels, not recomended to change
        "Screen size": (1280, 720),
        "Maximum FPS": 1000, # Reducing this could cause the program to be less precise
    },
    "Reaction time test": {
        "Cooldown time": 1000, # In milliseconds, a slight cooldown in the results and menu states so you don't accidentally click something
        "Minimum wait time": 100,
        "Maximum wait time": 3000,
        "Total trials": 20,
    },
    "Keybinds": {
        "Pressed events": [pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL], # Event types that the program checks for to know if you have pressed something
        "Exit keybinds": [pygame.K_ESCAPE, pygame.K_DELETE, pygame.K_LALT, pygame.K_RALT], # Press any of these keys to exit
        "Copy results": [pygame.K_r], # Press any of these keys to copy the results to clipboard
        "Copy settings": [pygame.K_s], # Press any of these keys to copy the settings to clipboard
    },
    "Colors": {
        "Menu": COLORS["black"],
        "Idle": COLORS["orange"],
        "Waiting": COLORS["green"],
        "Results": COLORS["navy"],
    },
    "Information": { # Don't change these
        "Menu title": "Welcome to...\nThe Reaction Time Test!",
        "Menu text": f"""You are currently on the menu.
Press any non-exit key to start!
On the left are some stats.
Press any exit key (see the left) to exit.
If the screen is:
- Menu (black): Click to start the test.
- Idle (orange): Wait for the screen to be waiting (green).
- Waiting (green): As soon as you can,
    - Click any button on your mouse. Or,
    - Press any non-keybinded key on your keyboard.
    - Pressing any exit key will return to the menu.
- Results (navy): Read your results. Click to return to menu.
Press R (default) to copy your results.
Press S (default) to copy the settings.
Copying only works if copying_enabled = True in the code.
If you have exited, you can change the settings in the code.""",
        "Idle title": "Idle",
        "Idle text": "Wait until the screen is waiting (green).",
        "Waiting title": "Waiting",
        "Waiting text": "Click or press as soon as you can!",
        "Results title": "Results.",
    }
}
SCREEN = pygame.display.set_mode(SETTINGS["Video"]["Screen size"], pygame.RESIZABLE)
pygame.display.set_caption("AaronMisc - Reaction Time Test")
CLOCK = pygame.time.Clock()
FONTS = {
    "basic": pygame.font.Font("freesansbold.ttf", SETTINGS["Video"]["Normal text size"]),
    "basic large": pygame.font.Font("freesansbold.ttf", SETTINGS["Video"]["Large text size"]),
}

def exit_pygame():
    pygame.quit()
    exit()

def draw_text(pos, text="Text", colour=COLORS["white"], font=FONTS["basic"], line_spacing=5, wrap_text=False, centred=False, surface=pygame.display.get_surface(), return_size=False):
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

def set_program_state(state):
    global background_colour, program_state, current_time, cooldown_time_end, trials_completed, time_to_wait, wait_times, waiting_start_time, game_start_time, game_end_time
    if state == "menu":
        background_colour = SETTINGS["Colors"]["Menu"]
        program_state = "menu"

        if "current_time" not in globals():
            current_time = 0
        
        cooldown_time_end = SETTINGS["Reaction time test"]["Cooldown time"] + current_time
        reset_program_variables()
    
    elif state == "idle":
        background_colour = SETTINGS["Colors"]["Idle"]
        program_state = "idle"
        time_to_wait_addon = randint(
                SETTINGS["Reaction time test"]["Minimum wait time"], 
                SETTINGS["Reaction time test"]["Maximum wait time"])
        wait_times.append(time_to_wait_addon)
        time_to_wait = time_to_wait_addon + current_time
    
    elif state == "waiting":
        background_colour = SETTINGS["Colors"]["Waiting"]
        program_state = "waiting"
        waiting_start_time = current_time
        waiting_start_times.append(waiting_start_time)
    
    elif state == "results":
        background_colour = SETTINGS["Colors"]["Results"]
        program_state = "results"
        cooldown_time_end = SETTINGS["Reaction time test"]["Cooldown time"] + current_time
        game_end_time = current_time

def reset_program_variables():
    global reaction_times, penalty_times, wait_times, waiting_start_times, trials_completed, waiting_start_time, game_start_time, game_end_time
    reaction_times = []
    penalty_times = []
    wait_times = []
    waiting_start_times = []
    trials_completed = 0
    waiting_start_time = 0
    game_start_time = 0
    game_end_time = 0

SCREEN.fill(COLORS["black"])
reset_program_variables()
set_program_state("menu")
time_to_wait = 0

while True:
    pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_pygame()

        elif event.type == pygame.KEYDOWN:
            if event.key in SETTINGS["Keybinds"]["Exit keybinds"]:
                if program_state in ["menu", "results"]:
                    exit_pygame()
                else:
                    set_program_state("menu")
            elif copying_enabled and event.key in SETTINGS["Keybinds"]["Copy results"]:
                if "results_text" in globals():
                    copy(results_text)
                else:
                    pass
            elif copying_enabled and event.key in SETTINGS["Keybinds"]["Copy settings"]:
                copy(SETTINGS)
            else:
                pressed = True

        elif event.type in SETTINGS["Keybinds"]["Pressed events"] and program_state not in ["menu", "results"]:
            pressed = True

    CLOCK.tick(SETTINGS["Video"]["Maximum FPS"])
    current_time = pygame.time.get_ticks()
    SCREEN.fill(background_colour)
    
    if program_state == "menu":
        if pressed and current_time > cooldown_time_end:
            set_program_state("idle")
            game_start_time = current_time

            if "results_text" in globals():
                del results_text
        
        draw_text((540, 10), SETTINGS["Information"]["Menu title"], font=FONTS["basic large"], surface=SCREEN)
        draw_text((540, 120), SETTINGS["Information"]["Menu text"], font=FONTS["basic"], surface=SCREEN)
    
    elif program_state == "idle":
        if pressed:
            penalty_times.append(current_time)
        
        if current_time > time_to_wait:
            set_program_state("waiting")
        
        draw_text((540, 10), SETTINGS["Information"]["Idle title"], font=FONTS["basic large"], surface=SCREEN)
        draw_text((540, 120), SETTINGS["Information"]["Idle text"], font=FONTS["basic"], surface=SCREEN)
        
    elif program_state == "waiting":
        if pressed:
            reaction_times.append(current_time - waiting_start_time)
            trials_completed += 1

            if trials_completed == SETTINGS["Reaction time test"]["Total trials"]:
                set_program_state("results")
            else:
                set_program_state("idle")
            
        draw_text((540, 10), SETTINGS["Information"]["Waiting title"], font=FONTS["basic large"], surface=SCREEN)
        draw_text((540, 120), SETTINGS["Information"]["Waiting text"], font=FONTS["basic"], surface=SCREEN)
        
    elif program_state == "results":
        if pressed and current_time > cooldown_time_end:
            set_program_state("menu")
        
        draw_text((540, 10), SETTINGS["Information"]["Results title"], font=FONTS["basic large"], surface=SCREEN)

        if "results_text" not in globals():
            try:
                results_text = f"""== Results ==
-- Reaction times (ms) --
Reaction time list: {reaction_times}.
Shortest reaction time: {min(reaction_times)}.
Longest reaction time: {max(reaction_times)}.
Total reaction time: {sum(reaction_times)}.
Average reaction time: {sum(reaction_times) / SETTINGS["Reaction time test"]["Total trials"]}.
Median reaction time: {statistics.median(reaction_times)}.
Standard deviation: {statistics.stdev(reaction_times)}.

-- Other times (ms) --
Penalty times: {penalty_times}
Number of penalties: {len(penalty_times)}.
Waiting times: {wait_times}.
Waiting start times: {waiting_start_times}.
Game start time: {game_start_time}.
Game end time: {game_end_time}.
Game duration: {game_end_time - game_start_time}.

-- Settings --
Total trials: {trials_completed}.

Press R to copy results to keyboard.
Press S to copy settings to keyboard.
Click to return to the menu."""
            except:
                results_text = "Error"
        
        draw_text((540, 120), results_text, font=FONTS["basic"], surface=SCREEN)
        
    display_text = f"""== Stats ==
-- Reaction time Test --
Pressed: {pressed}.
Current time: {f"{current_time} ms" if current_time < 1000000 else f"{current_time // 1000} s"}.
Waiting start time: {waiting_start_time} ms.
Trials completed: {trials_completed}.
Reaction times: {reaction_times if len(reaction_times) < 5 else f"...{reaction_times[-5:]}"}.
Penalty times: {penalty_times if len(penalty_times) < 5 else f"...{penalty_times[-5:]}."}

-- Program --
Program state: {program_state}.
Screen size: {SCREEN.get_size()}.
Exit keys: {"; ".join([pygame.key.name(key) for key in SETTINGS["Keybinds"]["Exit keybinds"]])}.
FPS: {int(CLOCK.get_fps())}."""
    
    draw_text((10, 10), display_text, font=FONTS["basic"], surface=SCREEN)
    
    pygame.display.update()
