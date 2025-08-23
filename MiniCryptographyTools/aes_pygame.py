from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyperclip
from aes_base import *
from pygame_simple_base import *

class AESWindow(Window):
    def __init__(self):
        super().__init__("AES Encryptor and Decryptor")

        self.page_state = "menu"
        self.show_debug = False

        self.create_buttons()

    def create_buttons(self):
        self.menu_buttons = pygame.sprite.Group(
            Button(x=10, y=80, w=600, h=150, heading_text="Encrypt Decrypt", body_text="Enter text to encrypt\nor decrypt using AES"),
            Button(x=10, y=240, w=600, h=150, heading_text="Generate Key", body_text="Generate a new AES key or\nconvert between string and hex"),
            Button(x=10, y=400, w=600, h=150, heading_text="Text File", body_text="Encrypt or decrypt a text file"),
            Button(x=10, y=560, w=600, h=150, heading_text="Credits", body_text="View credits"),
            Button(x=1070, y=615, w=200, h=100, heading_text="Quit", body_text="Close program")
        )

        self.encrypt_decrypt_buttons = pygame.sprite.Group(
            Button(x=10, y=615, w=200, h=100, heading_text="Encrypt", body_text="Encrypt text"),
            Button(x=220, y=615, w=200, h=100, heading_text="Decrypt", body_text="Decrypt text"),
            Button(x=430, y=615, w=400, h=100, heading_text="Copy", body_text="Copy output to clipboard"),
        )

        self.generate_key_buttons = pygame.sprite.Group(
            Button(x=10, y=615, w=200, h=100, heading_text="Hex", body_text="Generate a\nhex key"),
            Button(x=220, y=615, w=200, h=100, heading_text="Bytes", body_text="(Note: Not\nsupported)"),
            Button(x=430, y=615, w=200, h=100, heading_text="Base64", body_text="Generate a\nbase64 key"),
            Button(x=640, y=615, w=200, h=100, heading_text="Str to Hex", body_text="Convert string\nto hex"),
            Button(x=850, y=615, w=200, h=100, heading_text="Hex to Str", body_text="Convert hex\nto string"),
            Button(x=1060, y=615, w=200, h=100, heading_text="Copy", body_text="Copy output"),
        )

        self.text_file_buttons = pygame.sprite.Group(
            Button(x=10, y=615, w=200, h=100, heading_text="Encrypt", body_text="Encrypt text file"),
            Button(x=220, y=615, w=200, h=100, heading_text="Decrypt", body_text="Decrypt text file"),
            Button(x=430, y=615, w=400, h=100, heading_text="Copy", body_text="Copy output to clipboard"),
        )

        self.input_text_box = create_text_input_box(pos=(10, 100), dimentions=(600, 400), manager=self.ui_manager)
        self.output_text_box = create_text_input_box(pos=(620, 100), dimentions=(600, 400), manager=self.ui_manager)
        self.key_text_box = create_text_input_box(pos=(10, 540), dimentions=(600, 50), manager=self.ui_manager)

    def process_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_click = True
        else:
            self.mouse_click = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.page_state != "menu":
                    self.set_page_state("menu")
                else:
                    self.stop()
            
            if event.key == pygame.K_F3:
                self.show_debug = not self.show_debug
            
            if event.key == pygame.K_F9:
                self.set_page_state("encrypt decrypt")
            elif event.key == pygame.K_F10:
                self.set_page_state("generate key")
            elif event.key == pygame.K_F11:
                self.set_page_state("text file")
            elif event.key == pygame.K_F12:
                self.set_page_state("credits")

    def main_code(self):
        if self.page_state == "menu":
            draw_text((10, 10), "AES Encryptor and Decryptor", font=FONTS["title"], surface=self.display)

            self.menu_buttons.update()
            self.menu_buttons.draw(self.display)

            if self.mouse_click:
                for button in self.menu_buttons:
                    if button.is_clicked():
                        self.set_page_state(button.heading_text.lower())
        
        elif self.page_state == "encrypt decrypt":
            draw_text((10, 10), "Encrypt Decrypt", font=FONTS["title"], surface=self.display)

            draw_text((10, 80), f"Input Text", surface=self.display)
            draw_text((620, 80), f"Output Text", surface=self.display)
            draw_text((10, 520), f"Key", surface=self.display)

            self.encrypt_decrypt_buttons.update()
            self.encrypt_decrypt_buttons.draw(self.display)

            if self.mouse_click:
                for button in self.encrypt_decrypt_buttons:
                    if button.is_clicked():
                        if button.heading_text == "Encrypt":
                            try:
                                encrypted_text = encrypt(self.input_text_box.get_text(), self.key_text_box.get_text())
                            except Exception as e:
                                encrypted_text = f"Error: {e}"
                            self.output_text_box.set_text(encrypted_text)

                        elif button.heading_text == "Decrypt":
                            try:
                                decrypted_text = decrypt(self.input_text_box.get_text(), self.key_text_box.get_text())
                            except Exception as e:
                                decrypted_text = f"Error: {e}"
                            self.output_text_box.set_text(decrypted_text)

                        elif button.heading_text == "Copy":
                            pyperclip.copy(self.output_text_box.get_text())
      
        elif self.page_state == "generate key":
            draw_text((10, 10), "Generate Key", font=FONTS["title"], surface=self.display)

            draw_text((10, 80), f"Number of Bytes (note this should be 16 for this program to work)", surface=self.display)
            draw_text((10, 520), f"Key", surface=self.display)

            self.generate_key_buttons.update()
            self.generate_key_buttons.draw(self.display)

            if self.mouse_click:
                for button in self.generate_key_buttons:
                    if button.is_clicked():
                        error_occured = False
                        if button.heading_text in ["Hex", "Bytes", "Base64"]:
                            try:
                                number_of_bytes = int(self.input_text_box.get_text())
                                key = generate_key(number_of_bytes)
                            except Exception as e:
                                key = f"Error: {e}"
                                error_occured = True

                        if button.heading_text == "Hex":
                            if not error_occured:
                                key = key.hex()
                            self.output_text_box.set_text(key)
                            self.key_text_box.set_text(key)

                        elif button.heading_text == "Bytes":
                            if not error_occured:
                                key = str(key)
                            self.output_text_box.set_text(key)
                            self.key_text_box.set_text(key)

                        elif button.heading_text == "Base64":
                            if not error_occured:
                                key = bytes_to_base64(key)
                            self.output_text_box.set_text(key)
                            self.key_text_box.set_text(key)

                        elif button.heading_text == "Str to Hex":
                            hexed_string = self.input_text_box.get_text()
                            try:
                                hexed_string = string_to_hex(hexed_string)
                            except Exception as e:
                                hexed_string = f"Error: {e}"
                            self.output_text_box.set_text(hexed_string)

                        elif button.heading_text == "Hex to Str":
                            string_hex = self.input_text_box.get_text()
                            try:
                                string_hex = hex_to_string(string_hex)
                            except Exception as e:
                                string_hex = f"Error: {e}"
                            self.output_text_box.set_text(string_hex)

                        elif button.heading_text == "Copy":
                            pyperclip.copy(self.output_text_box.get_text())
        
        elif self.page_state == "text file":
            draw_text((10, 10), "Text File", font=FONTS["title"], surface=self.display)

            draw_text((10, 80), f"Text File Path", surface=self.display)
            draw_text((620, 80), f"Output Text", surface=self.display)
            draw_text((10, 520), f"Key", surface=self.display)
        
        elif self.page_state == "credits":
            draw_text((10, 10), "Credits", font=FONTS["title"], surface=self.display)

            draw_text((10, 80), f"Input Text", surface=self.display)
            draw_text((620, 80), f"Output Text", surface=self.display)
            draw_text((10, 520), f"Key", surface=self.display)
        
        if self.show_debug:
            draw_text((10, 600), f"Mouse Position: {pygame.mouse.get_pos()}. Page State: {self.page_state}.", surface=self.display)

    def set_page_state(self, page_state):
        self.page_state = page_state

        if page_state in ["menu", "credits"]:
            self.input_text_box.visible = False
            self.output_text_box.visible = False
            self.key_text_box.visible = False
        elif page_state in ["encrypt decrypt", "generate key", "text file"]:
            self.input_text_box.visible = True
            self.output_text_box.visible = True
            self.key_text_box.visible = True

def main():
    window = AESWindow()
    window.run()
 
if __name__ == "__main__":
    main()