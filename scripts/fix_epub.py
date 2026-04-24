import os
import re

files = ['index.html', 'index-jp.html']

for fpath in files:
    if not os.path.exists(fpath): continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # The language script is inside `coverPage`, `creditsPage`, `pageFiles`, `nav.xhtml` template literals.
    # We want to remove any <script> ... </script> block that appears inside those backticks.
    # Since we know the script exactly, we can use regex to remove it if it occurs after the first <script> block.
    # A safer way: find the EPUB generation functions and remove the <script> block from them.
    
    # Let's just find the script blocks that are inside backticks.
    # Or, notice that in the Python output, the script block is:
    # <script>\n    (function() {\n      try {\n        var savedLang = ...\n      } catch(e) {}\n    })();\n  </script>
    
    script_block = """<script>
    (function() {
      try {
        var savedLang = localStorage.getItem('threadborn_lang');
        if (!savedLang) return;
        var path = window.location.pathname;
        var isJp = path.indexOf('-jp') !== -1;
        
        if (savedLang === 'ja' && !isJp) {
          if (path === '/' || path === '/index' || path === '/index.html') {
            window.location.replace('./index-jp.html');
          } else if (path.indexOf('.html') !== -1) {
            window.location.replace(path.replace('.html', '-jp.html'));
          } else {
            window.location.replace(path + '-jp');
          }
        } else if (savedLang === 'en' && isJp) {
          if (path.indexOf('-jp.html') !== -1) {
            window.location.replace(path.replace('-jp.html', '.html'));
          } else {
            window.location.replace(path.replace('-jp', ''));
          }
        }
      } catch(e) {}
    })();
  </script>"""

    # We only want to keep the FIRST occurrence (in the actual <head>).
    # All subsequent occurrences should be removed.
    parts = content.split(script_block)
    
    if len(parts) > 1:
        new_content = parts[0] + script_block + "".join(parts[1:])
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {fpath} (removed {len(parts)-1} extra scripts)")

