import os
import re

files = ['index', 'login', 'signup', 'profile']

# The snippet to inject
lang_script = """<script>
  (function() {
    var savedLang = localStorage.getItem('threadborn_lang');
    var path = window.location.pathname;
    if (path.endsWith('/')) path += 'index.html';
    var isJp = path.indexOf('-jp.html') !== -1;
    if (savedLang === 'ja' && !isJp) {
      window.location.replace(path.replace('.html', '-jp.html'));
    } else if (savedLang === 'en' && isJp) {
      window.location.replace(path.replace('-jp.html', '.html'));
    }
  })();
</script>"""

for name in files:
    en_file = f"{name}.html"
    jp_file = f"{name}-jp.html"
    
    # Process EN file
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add script
        if "threadborn_lang" not in content:
            content = content.replace('<head>', f'<head>\n  {lang_script}')
            
        # Update link with onclick
        content = content.replace('href="./{name}-jp.html"'.format(name=name), f'href="./{name}-jp.html" onclick="localStorage.setItem(\'threadborn_lang\', \'ja\')"')
        content = content.replace(f'href="./{jp_file}"', f'href="./{jp_file}" onclick="localStorage.setItem(\'threadborn_lang\', \'ja\')"')
        
        # Update CSS
        content = re.sub(r'font-size:\s*clamp\(2\.4rem,\s*5\.4vw,\s*4\.1rem\);', r'font-size: clamp(1.8rem, 4vw, 2.8rem);', content)
        content = re.sub(r'max-width:\s*12ch;', r'max-width: 20ch;', content)
        content = re.sub(r'font-size:\s*clamp\(2\.5rem,\s*13vw,\s*3\.5rem\);', r'font-size: clamp(2rem, 10vw, 2.8rem);', content) # Mobile size
        
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    # Process JP file
    if os.path.exists(jp_file):
        with open(jp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add script
        if "threadborn_lang" not in content:
            content = content.replace('<head>', f'<head>\n  {lang_script}')
            
        # Update link with onclick
        content = content.replace('href="./{name}.html"'.format(name=name), f'href="./{name}.html" onclick="localStorage.setItem(\'threadborn_lang\', \'en\')"')
        content = content.replace(f'href="./{en_file}"', f'href="./{en_file}" onclick="localStorage.setItem(\'threadborn_lang\', \'en\')"')
        
        # Update CSS
        content = re.sub(r'font-size:\s*clamp\(2\.4rem,\s*5\.4vw,\s*4\.1rem\);', r'font-size: clamp(1.8rem, 4vw, 2.8rem);', content)
        content = re.sub(r'max-width:\s*12ch;', r'max-width: 20ch;', content)
        content = re.sub(r'font-size:\s*clamp\(2\.5rem,\s*13vw,\s*3\.5rem\);', r'font-size: clamp(2rem, 10vw, 2.8rem);', content) # Mobile size
        
        with open(jp_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Updated UI and lang scripts.")
