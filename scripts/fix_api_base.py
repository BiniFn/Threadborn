import os
import re

TARGET_FILES = [
    "login.html", "login-jp.html",
    "signup.html", "signup-jp.html",
    "profile.html", "profile-jp.html",
    "index.html", "index-jp.html",
    "assets/phase1-client.js"
]

def fix_file(filepath):
    if not os.path.exists(filepath):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The existing block looks like:
    #      if (host === "appassets.androidplatform.net") {
    #        return "https://threadborn.vercel.app";
    #      }
    
    new_content = re.sub(
        r'if\s*\(\s*host\s*===\s*"appassets\.androidplatform\.net"\s*\)\s*\{',
        'if (host === "appassets.androidplatform.net" || window.location.protocol === "file:") {',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {filepath}")

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".html") or file.endswith(".js"):
            full_path = os.path.join(root, file)
            # Only process if it has resolveApiBase
            with open(full_path, 'r', encoding='utf-8') as f:
                try:
                    content = f.read()
                    if "resolveApiBase" in content and "appassets.androidplatform.net" in content:
                        if '|| window.location.protocol === "file:"' not in content and "|| window.location.protocol === 'file:'" not in content:
                            new_content = re.sub(
                                r'if\s*\(\s*host\s*===\s*[\'"]appassets\.androidplatform\.net[\'"]\s*\)\s*\{',
                                'if (host === "appassets.androidplatform.net" || window.location.protocol === "file:") {',
                                content
                            )
                            with open(full_path, 'w', encoding='utf-8') as fw:
                                fw.write(new_content)
                            print(f"Fixed {full_path}")
                except Exception:
                    pass

print("Done fixing API bases.")
