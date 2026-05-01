import re

def update_html(filepath, is_jp=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Banners
    # Replace announcement banner
    old_banner = r'<div id="global-announcement-banner" class="global-banner" style="display:none;[^"]*"></div>'
    new_banner = '<div id="global-announcement-banner" class="global-banner" style="display:none;"></div>'
    content = re.sub(old_banner, new_banner, content)

    # Replace countdown banner
    old_countdown = r'<div id="global-countdown-banner" class="global-banner" style="display:none;[^"]*">\s*<span id="global-countdown-title"></span>:\s*<span id="global-countdown-timer" style="color:#ff6b6b;"></span>\s*</div>'
    new_countdown = '''<div id="global-countdown-banner" class="global-banner" style="display:none; border-color: rgba(255, 107, 107, 0.4);">
      <span id="global-countdown-title"></span>: 
      <span id="global-countdown-timer" style="color:#ff6b6b; font-family: \'Space Mono\', monospace;"></span>
    </div>
    <div id="global-polls-container"></div>'''
    
    # Check if polls container already exists
    if 'id="global-polls-container"' not in content:
        content = re.sub(old_countdown, new_countdown, content)
    else:
        # Just update countdown
        content = re.sub(r'<div id="global-countdown-banner".*?</div>', 
                         '''<div id="global-countdown-banner" class="global-banner" style="display:none; border-color: rgba(255, 107, 107, 0.4);">
      <span id="global-countdown-title"></span>: 
      <span id="global-countdown-timer" style="color:#ff6b6b; font-family: \'Space Mono\', monospace;"></span>
    </div>''', content, flags=re.DOTALL)

    # 2. Replace Dashboard Section
    # Find section id="view-dashboard"
    dashboard_start = content.find('<section id="view-dashboard" class="view">')
    dashboard_end = content.find('</section>', dashboard_start) + len('</section>')
    
    title = "ダッシュボード" if is_jp else "Owner Dashboard"
    desc = "サイトコンテンツ、グローバルアナウンス、アートギャラリーを管理します。" if is_jp else "Manage site content, global announcements, and art gallery."
    announcement_label = "グローバルアナウンス" if is_jp else "Global Announcement"
    announcement_desc = "メインメニューの上部に表示されるバナーを設定します。" if is_jp else "Set a persistent banner at the top of the main menus."
    countdown_label = "グローバルカウントダウン" if is_jp else "Global Countdown"
    art_label = "アートのアップロード" if is_jp else "Upload Art"
    art_desc = "Drawingsギャラリーに新しいアートを追加します。" if is_jp else "Add new art to the Drawings gallery."
    save_btn = "設定を保存" if is_jp else "Save Config"
    upload_btn = "アップロード" if is_jp else "Upload Art"
    clear_btn = "削除" if is_jp else "Clear"
    poll_label = "投票の管理" if is_jp else "Manage Polls"
    poll_desc = "読者向けの投票を作成または削除します。" if is_jp else "Create or delete polls for readers."
    create_poll_btn = "投票を作成" if is_jp else "Create Poll"
    lang_sel_en = "英語サイト (English Site)"
    lang_sel_ja = "日本語サイト (Japanese Site)"

    new_dashboard = f'''<section id="view-dashboard" class="view">
      <div class="section-head">
        <div>
          <h2>{title}</h2>
          <p class="section-copy">{desc}</p>
        </div>
      </div>
      
      <div style="margin-bottom: 24px; text-align: center;">
        <label style="margin-right: 12px; font-family: 'Space Mono', monospace;">Config Target:</label>
        <select id="dashboard-target-lang" style="padding: 8px; border-radius: 4px; background: #222; color: #fff; border: 1px solid #444;" onchange="loadDashboardConfig()">
          <option value="en" {"" if is_jp else "selected"}>{lang_sel_en}</option>
          <option value="ja" {"selected" if is_jp else ""}>{lang_sel_ja}</option>
        </select>
      </div>

      <div class="grid">
        <article class="card">
          <h3>{announcement_label}</h3>
          <p>{announcement_desc}</p>
          <div class="input-row">
            <input type="text" id="dashboard-announcement" placeholder="Announcement text..." style="padding:8px;" />
            <button class="btn-clear" onclick="clearDashboardAnnouncement()">{clear_btn}</button>
          </div>
          <button class="nav-btn" onclick="saveDashboardConfig()">{save_btn}</button>
        </article>
        
        <article class="card">
          <h3>{countdown_label}</h3>
          <div class="input-row">
            <input type="text" id="dashboard-countdown-title" placeholder="Countdown Title..." style="padding:8px;" />
            <button class="btn-clear" onclick="clearDashboardTimer()">{clear_btn}</button>
          </div>
          <input type="datetime-local" id="dashboard-countdown-date" style="width:100%; margin-bottom:10px; padding:8px;" />
          <button class="nav-btn" onclick="saveDashboardConfig()">{save_btn}</button>
        </article>
        
        <article class="card" style="grid-column: 1 / -1;">
          <h3>{poll_label}</h3>
          <p>{poll_desc}</p>
          <div class="input-row">
            <input type="text" id="dashboard-poll-question" placeholder="Poll Question..." style="padding:8px;" />
          </div>
          <div id="dashboard-poll-options">
            <input type="text" class="dashboard-poll-opt" placeholder="Option 1" style="width:100%; margin-bottom:8px; padding:8px;" />
            <input type="text" class="dashboard-poll-opt" placeholder="Option 2" style="width:100%; margin-bottom:8px; padding:8px;" />
            <input type="text" class="dashboard-poll-opt" placeholder="Option 3 (Optional)" style="width:100%; margin-bottom:8px; padding:8px;" />
            <input type="text" class="dashboard-poll-opt" placeholder="Option 4 (Optional)" style="width:100%; margin-bottom:10px; padding:8px;" />
          </div>
          <button class="nav-btn" onclick="createPoll()">{create_poll_btn}</button>
          <p id="dashboard-poll-status" style="margin-top:10px;font-size:12px;"></p>
          <div id="dashboard-active-polls-list" style="margin-top: 16px;"></div>
        </article>

        <article class="card">
          <h3>{art_label}</h3>
          <p>{art_desc}</p>
          <input type="text" id="dashboard-art-char" placeholder="Character Name (e.g. Yono)" style="width:100%; margin-bottom:10px; padding:8px;" />
          <input type="text" id="dashboard-art-label" placeholder="Label (e.g. Official Concept)" style="width:100%; margin-bottom:10px; padding:8px;" />
          <input type="file" id="dashboard-art-file" accept="image/*" style="margin-bottom:10px;" />
          <button class="nav-btn" onclick="uploadDashboardArt()">{upload_btn}</button>
          <p id="dashboard-art-status" style="margin-top:10px;font-size:12px;"></p>
        </article>
      </div>
    </section>'''
    
    content = content[:dashboard_start] + new_dashboard + content[dashboard_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_html('index.html', False)
update_html('index-jp.html', True)
print("Updated index.html and index-jp.html")
