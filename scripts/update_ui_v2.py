import os
import re

files = ['index']

for name in files:
    en_file = f"{name}.html"
    jp_file = f"{name}-jp.html"
    
    # Process EN file
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update CSS
        content = re.sub(r'font-size:\s*clamp\(1\.8rem,\s*4vw,\s*2\.8rem\);', r'font-size: clamp(1.4rem, 2.5vw, 2.2rem);', content)
        content = re.sub(r'font-size:\s*clamp\(2\.4rem,\s*5\.4vw,\s*4\.1rem\);', r'font-size: clamp(1.4rem, 2.5vw, 2.2rem);', content)
        content = re.sub(r'font-size:\s*clamp\(2rem,\s*10vw,\s*2\.8rem\);', r'font-size: clamp(1.6rem, 7vw, 2.2rem);', content)
        content = re.sub(r'font-size:\s*clamp\(2\.5rem,\s*13vw,\s*3\.5rem\);', r'font-size: clamp(1.6rem, 7vw, 2.2rem);', content)
        
        # Inject button in hero-actions if not there
        if "Switch to Japanese" not in content:
            hero_actions_block = """<div class="hero-actions">
              <button class="btn btn-primary" onclick="openChapter(0)">Start Reading</button>
              <button class="btn btn-secondary" onclick="localStorage.setItem('threadborn_lang', 'ja'); window.location.href='./index-jp.html'">🇯🇵 Switch to Japanese</button>"""
            content = re.sub(r'<div class="hero-actions">\s*<button class="btn btn-primary" onclick="openChapter\(0\)">Start Reading</button>', hero_actions_block, content)
            
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    # Process JP file
    if os.path.exists(jp_file):
        with open(jp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update CSS
        content = re.sub(r'font-size:\s*clamp\(1\.8rem,\s*4vw,\s*2\.8rem\);', r'font-size: clamp(1.4rem, 2.5vw, 2.2rem);', content)
        content = re.sub(r'font-size:\s*clamp\(2\.4rem,\s*5\.4vw,\s*4\.1rem\);', r'font-size: clamp(1.4rem, 2.5vw, 2.2rem);', content)
        content = re.sub(r'font-size:\s*clamp\(2rem,\s*10vw,\s*2\.8rem\);', r'font-size: clamp(1.6rem, 7vw, 2.2rem);', content)
        content = re.sub(r'font-size:\s*clamp\(2\.5rem,\s*13vw,\s*3\.5rem\);', r'font-size: clamp(1.6rem, 7vw, 2.2rem);', content)
        
        # Inject button in hero-actions if not there
        if "English Version" not in content:
            hero_actions_block = """<div class="hero-actions">
              <button class="btn btn-primary" onclick="openChapter(0)">Start Reading</button>
              <button class="btn btn-secondary" onclick="localStorage.setItem('threadborn_lang', 'en'); window.location.href='./index.html'">🇺🇸 English Version</button>"""
            content = re.sub(r'<div class="hero-actions">\s*<button class="btn btn-primary" onclick="openChapter\(0\)">Start Reading</button>', hero_actions_block, content)
            
            # Or if it was already translated to Japanese "Start Reading" text
            hero_actions_block_jp = """<div class="hero-actions">
              <button class="btn btn-primary" onclick="openChapter(0)">Start Reading</button>
              <button class="btn btn-secondary" onclick="localStorage.setItem('threadborn_lang', 'en'); window.location.href='./index.html'">🇺🇸 English Version</button>"""
            content = re.sub(r'<div class="hero-actions">\s*<button class="btn btn-primary" onclick="openChapter\(0\)">.*?<', hero_actions_block_jp + '<', content)

        with open(jp_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Updated UI V2 successfully.")
