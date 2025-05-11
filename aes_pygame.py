from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import pyperclip
from aes_base import *
from pygame_simple_base import *

class AESWindow(Window):
    def __init__(self, display_name = "Display", dimensions = (1280, 720)):
        super().__init__(display_name, dimensions)

    def process_events(self, event):
        pass

    def main_code(self):
        pass
