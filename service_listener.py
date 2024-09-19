import ctypes
import ctypes.wintypes
import keyboard
import pyperclip
import subprocess
import time
import os
import configparser

layout_to_lang = {
    '0x409': 'en',  # English (US)
    '0x809': 'en',  # English (UK)
    '0x40d': 'he',  # Hebrew
    '0x419': 'ru',  # Russian
    '0x401': 'ar',  # Arabic
    '0x2c01': 'ar',  # Arabic (Jordan)
    '0xc01': 'ar',  # Arabic (Egypt)
    '0x801': 'ar',  # Arabic (iraq)
    '0x3001': 'ar',  # Arabic (Lebanon)
}


def get_keyboard_layouts():
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    # Get the number of keyboard layouts
    n_layouts = user32.GetKeyboardLayoutList(0, None)

    # Create an array to hold the layouts
    layouts = (ctypes.wintypes.HKL * n_layouts)()
    user32.GetKeyboardLayoutList(n_layouts, layouts)

    installed_layouts = []
    for layout in layouts:
        layout_id = hex(layout & (2 ** 16 - 1))  # Extract the lower 16 bits which hold the language identifier
        installed_layouts.append(layout_id)

    return installed_layouts


def get_language_list(layout_codes):
    return [layout_to_lang[layout] for layout in layout_codes if layout in layout_to_lang]


def run_external_script(input_text):
    script_path = os.path.join(os.path.dirname(__file__), 'convert_en_and_heb.py')
    try:
        result = subprocess.run(
            ['python', script_path, input_text,','.join(layouts)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception: {e}")
        return str(e)

def on_hotkey_pressed():
    try:
        original_clipboard_content = pyperclip.paste()
        keyboard.send('ctrl+c')
        time.sleep(0.2)
        selected_text = pyperclip.paste()

        if selected_text:
            processed_text = run_external_script(selected_text)
            pyperclip.copy(processed_text)
            keyboard.send('ctrl+v')

        else:
            print("No text selected.")
        time.sleep(0.2)
        pyperclip.copy(original_clipboard_content)

    except Exception as e:
        print(f"Exception: {e}")


def read_hotkey_from_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['HOTKEYS'].get('hot_keys')


layouts = get_language_list(get_keyboard_layouts())
hotkey = read_hotkey_from_config("config.ini")

keyboard.add_hotkey(hotkey, on_hotkey_pressed)
print(f"Service is running. Press {hotkey} to process selected text.")
keyboard.wait()
