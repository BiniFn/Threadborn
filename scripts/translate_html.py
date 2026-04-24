import os
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='ja')

def translate_body_text(filepath):
    print(f"Translating {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # We only want to translate nodes inside <main>, <header>, <nav>
    # but skip anything inside <script>
    
    translate_targets = []
    
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        # Skip scripts, styles, etc.
        if parent.name in ['script', 'style', 'head', 'title', 'meta']:
            continue
            
        # We only want to translate English text
        text = text_node.string
        if text and text.strip() and len(text.strip()) > 1:
            # Check if it has english characters
            if any(c.isalpha() and ord(c) < 128 for c in text):
                translate_targets.append(text_node)

    print(f"Found {len(translate_targets)} nodes to translate.")
    
    for node in translate_targets:
        text = node.string
        try:
            # preserve leading/trailing whitespace
            stripped = text.strip()
            translated = translator.translate(stripped)
            prefix = text[:len(text) - len(text.lstrip())]
            suffix = text[len(text.rstrip()):]
            node.replace_with(NavigableString(prefix + translated + suffix))
        except Exception as e:
            print(f"Failed to translate: {stripped} - {e}")
            pass

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Done translating {filepath}.")

translate_body_text('index-jp.html')
translate_body_text('login-jp.html')
translate_body_text('signup-jp.html')
translate_body_text('profile-jp.html')
