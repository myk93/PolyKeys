import ctypes
import locale

user32 = ctypes.WinDLL('user32', use_last_error=True)

en_to_he = {
    'q': '/', 'w': '\'', 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ',

    'Q': '/', 'W': '"', 'E': 'ק', 'R': 'ר', 'T': 'א', 'Y': 'ט', 'U': 'ו', 'I': 'ן', 'O': 'ם', 'P': 'פ',
    'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י', 'J': 'ח', 'K': 'ל', 'L': 'ך',
    'Z': 'ז', 'X': 'ס', 'C': 'ב', 'V': 'ה', 'B': 'נ', 'N': 'מ', 'M': 'צ'
}

LANGUAGE_IDS = {
    'en_US': 0x0409,  # English US
    'he_IL': 0x040D  # Hebrew Israel
}


def get_current_keyboard_layout():
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    lang_id = layout_id & (2 ** 16 - 1)
    locale_name = locale.windows_locale.get(lang_id, f"Unknown locale (ID: {lang_id})")
    return locale_name

def convert_en_to_he(text):
    return ''.join(en_to_he.get(char, char) for char in text)

english_text = "shalom"
hebrew_text = convert_en_to_he(english_text)
print(hebrew_text)

צצצ

