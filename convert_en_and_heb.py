import io
import sys
import ctypes
import ctypes.wintypes

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

en_to_he = {
    'q': '/', 'w': '\'', 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ', '/': '.',
    ';': 'ף', '\'': ',',
}

he_to_en = {v: k for k, v in en_to_he.items()}

en_to_ru = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
    'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
    'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',
    ';': 'ж', '\'': 'э',
}

ru_to_en = {v: k for k, v in en_to_ru.items()}

en_to_ar = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ي', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    'z': 'ط', 'x': 'ك', 'c': 'ذ', 'v': 'ز', 'b': 'ر', 'n': 'و', 'm': 'ى', ',': 'ة', '.': 'گ', '/': '/',
    ';': 'ظ', '\'': 'ل',
}

ar_to_en = {v: k for k, v in en_to_ar.items()}

# Conversion functions
def translate(text, translation_dict):
    return ''.join(translation_dict.get(char, char) for char in text)

def translate_via_intermediate(text, source_to_intermediate, intermediate_to_target):
    intermediate_text = translate(text, source_to_intermediate)
    return translate(intermediate_text, intermediate_to_target)

def detect_language(text):
    # Define character sets for Hebrew, Arabic, and Russian
    hebrew_chars = set('אבגדהוזחטיכלמנסעפצקרשתםןףךץ')
    arabic_chars = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويء')
    russian_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

    hebrew_count = sum(1 for char in text if char in hebrew_chars)
    arabic_count = sum(1 for char in text if char in arabic_chars)
    russian_count = sum(1 for char in text if char in russian_chars)
    max_count = max(hebrew_count, arabic_count, russian_count)

    if max_count == hebrew_count and hebrew_count > 0:
        return 'he'
    elif max_count == arabic_count and arabic_count > 0:
        return 'ar'
    elif max_count == russian_count and russian_count > 0:
        return 'ru'
    else:
        return 'en'


def convert_text(text, from_language, to_language):
    translation_dicts = {
        ('en', 'he'): en_to_he,
        ('he', 'en'): he_to_en,
        ('en', 'ru'): en_to_ru,
        ('ru', 'en'): ru_to_en,
        ('ar', 'en'): ar_to_en,
        ('en', 'ar'): en_to_ar,
    }

    translation_dict = translation_dicts.get((from_language, to_language))

    if translation_dict:
        return translate(text, translation_dict)
    else:
        from_to_eng = translation_dicts.get((from_language, 'en'))
        eng_to_target = translation_dicts.get(('en', to_language))
        return translate_via_intermediate(text, from_to_eng, eng_to_target)

layout_to_lang = {
    '0x409': 'en',  # English (US)
    '0x809': 'en',  # English (UK)
    '0x40d': 'he',  # Hebrew
    '0x401': 'ar',  # Arabic
    '0x419': 'ru'   # Russian
}
#
# def get_keyboard_layouts():
#     user32 = ctypes.WinDLL('user32', use_last_error=True)
#
#     # Get the number of keyboard layouts
#     n_layouts = user32.GetKeyboardLayoutList(0, None)
#
#     # Create an array to hold the layouts
#     layouts = (ctypes.wintypes.HKL * n_layouts)()
#     user32.GetKeyboardLayoutList(n_layouts, layouts)
#
#     installed_layouts = []
#     for layout in layouts:
#         layout_id = hex(layout & (2 ** 16 - 1))  # Extract the lower 16 bits which hold the language identifier
#         installed_layouts.append(layout_id)
#
#     return installed_layouts
#
# def get_language_list(layout_codes):
#     return [layout_to_lang.get(layout) for layout in layout_codes]
#
#
def get_next_language(languages, lang):
    current_index = languages.index(lang)
    next_language = languages[(current_index + 1) % len(languages)]
    return next_language


if __name__ == "__main__":
    input_text = sys.argv[1]
    all_layouts_installed = sys.argv[2].split(',')
    lines = input_text.splitlines()

    converted_lines = []

    for line in lines:
        detected_language = detect_language(line)
        next_language = get_next_language(all_layouts_installed, detected_language)
        converted_line = convert_text(line, detected_language, next_language)
        converted_lines.append(converted_line)

    converted_text = '\n'.join(converted_lines)

    print(converted_text)
