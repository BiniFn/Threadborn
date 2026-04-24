import os

files = ['index', 'login', 'signup', 'profile']

translations = {
    'Home': 'ホーム',
    'Volumes': '巻数',
    'Chapters': 'チャプター',
    'App': 'アプリ',
    'Characters': 'キャラクター',
    'Powers': '能力',
    'Leaks': 'リーク',
    'Lore': '設定・伝承',
    'Drawings': 'イラスト',
    'Credits': 'クレジット',
    'Login': 'ログイン',
    'Sign Up': 'サインアップ',
    'Profile': 'プロフィール',
    'Logout': 'ログアウト',
    'Guest reader': 'ゲスト読者',
    'Entering Lumera': 'ルメラにアクセス中',
    'Loading the reader, chapters, and collector tools.': 'リーダー、チャプター、コレクターツールを読み込んでいます。'
}

for name in files:
    en_file = f"{name}.html"
    jp_file = f"{name}-jp.html"
    
    # Update English files to include language switcher
    with open(en_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'id="lang-jp"' not in content:
        content = content.replace('</nav>', f'  <a class="nav-btn" id="lang-jp" href="./{jp_file}">JP</a>\n      </nav>')
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    # Update Japanese files
    with open(jp_file, 'r', encoding='utf-8') as f:
        jp_content = f.read()
        
    jp_content = jp_content.replace('lang="en"', 'lang="ja"')
    
    if 'id="lang-en"' not in jp_content:
        jp_content = jp_content.replace('</nav>', f'  <a class="nav-btn" id="lang-en" href="./{en_file}">EN</a>\n      </nav>')
        
    for en_text, jp_text in translations.items():
        jp_content = jp_content.replace(f'>{en_text}<', f'>{jp_text}<')
        
    with open(jp_file, 'w', encoding='utf-8') as f:
        f.write(jp_content)
        
print("Successfully processed HTML files.")
