import os
import re

files = ['index', 'login', 'signup', 'profile']

for name in files:
    for ext in ['.html', '-jp.html']:
        fname = f"{name}{ext}"
        if not os.path.exists(fname): continue
        
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fix double onclick
        content = content.replace('onclick="localStorage.setItem(\'threadborn_lang\', \'ja\')" onclick="localStorage.setItem(\'threadborn_lang\', \'ja\')"', 'onclick="localStorage.setItem(\'threadborn_lang\', \'ja\')"')
        content = content.replace('onclick="localStorage.setItem(\'threadborn_lang\', \'en\')" onclick="localStorage.setItem(\'threadborn_lang\', \'en\')"', 'onclick="localStorage.setItem(\'threadborn_lang\', \'en\')"')
        
        # Remove all lang_script injections
        script_pattern = re.compile(r'<script>\s*\(function\(\) \{\s*var savedLang = localStorage\.getItem\(\'threadborn_lang\'\);.*?\s*\}\)\(\);\s*</script>\n  ', re.DOTALL)
        content = script_pattern.sub('', content)
        
        # Inject script only at the FIRST <head>
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
        
        content = content.replace('<head>', f'<head>\n  {lang_script}', 1)
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

print("Cleaned up files.")
