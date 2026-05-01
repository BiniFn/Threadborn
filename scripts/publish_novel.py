import sys
import re
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def inline_md_to_html(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    return escaped

def content_blocks(content: str):
    raw_blocks = re.split(r"\n\s*\n", content)
    return [b.strip() for b in raw_blocks if b.strip() and b.strip() != "***"]

def chapter_pages(chapter, jp=False):
    if chapter["volume_num"] == 3:
        number_label = (
            f'EX小説 第{chapter["chapter_num"]:02d}章'
            if jp
            else f'EX Novel · Chapter {chapter["chapter_num"]:02d}'
        )
    else:
        number_label = (
            f'第{chapter["volume_num"]:02d}巻 · 第{chapter["chapter_num"]:02d}章'
            if jp
            else f'Volume {chapter["volume_num"]:02d} · Chapter {chapter["chapter_num"]:02d}'
        )
    head = f'''<div class="chapter-head">
  <span class="chapter-num">{number_label}</span>
  <h2 class="chapter-title">{html.escape(chapter["title"])}</h2>
  <p class="chapter-subtitle">{inline_md_to_html(chapter["subtitle"])}</p>
</div>'''
    html_blocks = [head]
    for block in content_blocks(chapter["content"]):
        if block.startswith("##"):
            continue
        if block.startswith("*Volume") or block.startswith("*EX"):
            continue
        if block.startswith("### "):
            html_blocks.append(f'<p class="scene-title">{inline_md_to_html(block[4:].strip())}</p>')
        elif block.startswith(">"):
            lines = [ln.strip()[1:].strip() if ln.strip().startswith(">") else ln.strip() for ln in block.splitlines()]
            title = lines[0] if lines else "Status"
            body = "<br>".join(inline_md_to_html(ln) for ln in lines[1:])
            html_blocks.append(f'<div class="system-box"><h5>{inline_md_to_html(title).replace("<em>", "").replace("</em>", "")}</h5><p>{body}</p></div>')
        elif re.match(r"^\*End of Chapter\s+\d+\*$", block, re.I):
            html_blocks.append(f'<div class="tbc">End of Chapter {chapter["chapter_num"]:02d}</div>')
        elif re.match(r"^\*第\d+章", block):
            html_blocks.append(f'<div class="tbc">{inline_md_to_html(block.strip("*"))}</div>')
        else:
            paragraph = inline_md_to_html(block).replace("\n", "<br>")
            html_blocks.append(f'<p class="novel-p">{paragraph}</p>')

    pages = []
    current = []
    p_count = 0
    for block in html_blocks:
        current.append(block)
        if 'class="novel-p"' in block:
            p_count += 1
        if p_count >= 12:
            pages.append("\n".join(current))
            current = []
            p_count = 0
    if current:
        pages.append("\n".join(current))
    return pages

def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)

def js_template(value: str) -> str:
    return "`" + value.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${") + "`"

def chapter_js_data(chapters, jp=False):
    legacy_items = []
    chapter_items = []
    for ch in chapters:
        pages = chapter_pages(ch, jp=jp)
        pages_js = "[\n" + ",\n".join("          " + js_template(p) for p in pages) + "\n        ]"
        if ch["volume_num"] == 1:
            legacy_label = (
                f'第{ch["chapter_num"]:02d}章 · {ch["title"]}'
                if jp
                else f'Chapter {ch["chapter_num"]:02d} · {ch["title"]}'
            )
            legacy_items.append(f'''  {{
    label: {js_string(legacy_label)},
    pages: {pages_js}
  }}''')
        page_ref = f"legacyEpisodes[{ch['chapter_num'] - 1}].pages" if ch["volume_num"] == 1 else pages_js
        if ch["volume_num"] == 3:
            volume_label = "EX Novel Vol 1" if not jp else "EX小説 第1巻"
        else:
            volume_label = f"Volume {ch['volume_num']}" if not jp else f"第{ch['volume_num']}巻"
            
        chapter_label = f"Chapter {ch['chapter_num']}" if not jp else f"第{ch['chapter_num']}章"
        label = ch["chapter_heading"]
        item = f'''      {{
        volume: {js_string(volume_label)},
        chapter: {js_string(chapter_label)},
        label: {js_string(label)},
        title: {js_string(ch["title"])},
        summary: {js_string(ch["subtitle"])},
        tags: [{js_string("story")}],
        pages: {page_ref}
      }}'''
        chapter_items.append(item)
    return "    const legacyEpisodes = [\n" + ",\n".join(legacy_items) + "\n    ];\n\n    const chapters = [\n" + ",\n".join(chapter_items) + "\n    ];\n\n"

def replace_story_data(html_text: str, data_js: str) -> str:
    start = html_text.index("    const legacyEpisodes = [")
    end = html_text.index("    const characters = [")
    return html_text[:start] + data_js + html_text[end:]

def parse_chapters(md: str):
    lines = md.splitlines()
    chapters = []
    current_volume = None
    current_volume_title = None
    i = 0
    while i < len(lines):
        line = lines[i]
        vm = re.match(r"^#\s+(.+)$", line)
        if vm and ("Volume" in vm.group(1) or "巻" in vm.group(1) or "EX" in vm.group(1)):
            current_volume_title = vm.group(1).strip()
            if "EX" in current_volume_title:
                current_volume = 3
            else:
                vol_match = re.search(r"Volume\s+(\d+)", current_volume_title)
                if not vol_match:
                    vol_match = re.search(r"第\s*(\d+)\s*巻", current_volume_title)
                current_volume = int(vol_match.group(1)) if vol_match else 1
            i += 1
            continue
        
        # Case insensitive match for Chapter
        cm = re.match(r"^##\s+Chapter\s+(\d+):\s+(.+)$", line, re.I)
        if not cm:
            cm = re.match(r"^##\s+第\s*(\d+)\s*章[:：]?\s*(.+)$", line)
        if not cm:
            i += 1
            continue

        ch_num = int(cm.group(1))
        fallback_title = cm.group(2).strip()
        start = i
        i += 1
        section = []
        while i < len(lines):
            if (
                re.match(r"^##\s+Chapter\s+\d+:", lines[i], re.I)
                or re.match(r"^##\s+第\s*\d+\s*章", lines[i])
                or re.match(r"^#\s+.+Volume\s+\d+", lines[i])
                or re.match(r"^#\s+.+第\s*\d+\s*巻", lines[i])
                or re.match(r"^#\s+.+EX", lines[i])
            ):
                break
            section.append(lines[i])
            i += 1

        title = fallback_title
        subtitle = ""
        content_start = 0
        for idx, sline in enumerate(section):
            if re.match(r"^##\s+", sline) and "Chapter" not in sline and "章" not in sline:
                title = sline.replace("##", "", 1).strip()
                content_start = idx + 1
                break
        for idx in range(content_start, len(section)):
            sline = section[idx].strip()
            if sline.startswith("*Volume") or sline.startswith("*EX"):
                continue
            if sline.startswith("*") and sline.endswith("*") and "End of Chapter" not in sline and "終わり" not in sline:
                subtitle = sline.strip("*").strip()
                content_start = idx + 1
                break

        content = "\n".join(section[content_start:]).strip()
        chapters.append({
            "volume_num": current_volume or 1,
            "volume_title": current_volume_title or "",
            "chapter_num": ch_num,
            "chapter_heading": fallback_title,
            "title": title,
            "subtitle": subtitle,
            "content": content,
        })

    return chapters

def main():
    en_md = (ROOT / "Threadborn-Complete.md").read_text(encoding="utf-8")
    ex_md = (ROOT / "Threadborn-EX.md").read_text(encoding="utf-8")
    # Make EX md look like a volume with a single chapter
    ex_md = ex_md.replace("## EX NOVEL VOL 1", "# EX Novel Vol 1\n\n## Chapter 1: The Chronicle Beyond the Chapter", 1)
    # Downgrade all other chapters in EX so they aren't parsed as separate chapters
    ex_md = re.sub(r"^##\s+CHAPTER", "### CHAPTER", ex_md, flags=re.MULTILINE | re.IGNORECASE)
    
    ja_md = (ROOT / "Threadborn-Complete-JP.md").read_text(encoding="utf-8")
    ex_ja_md = (ROOT / "Threadborn-EX-JP.md").read_text(encoding="utf-8")
    ex_ja_md = ex_ja_md.replace("## EX小説 第1巻", "# EX小説 第1巻\n\n## 第1章：章を超えたクロニクル", 1)
    ex_ja_md = re.sub(r"^##\s+第\s*\d+\s*章", "### 第", ex_ja_md, flags=re.MULTILINE)

    en_combined = en_md + "\n\n" + ex_md
    ja_combined = ja_md + "\n\n" + ex_ja_md

    en_chaps = parse_chapters(en_combined)
    ja_chaps = parse_chapters(ja_combined)
    
    # Update EN html
    html_en = (ROOT / "index.html").read_text(encoding="utf-8")
    html_en = replace_story_data(html_en, chapter_js_data(en_chaps, jp=False))
    (ROOT / "index.html").write_text(html_en, encoding="utf-8")

    # Update JP html
    html_ja = (ROOT / "index-jp.html").read_text(encoding="utf-8")
    html_ja = replace_story_data(html_ja, chapter_js_data(ja_chaps, jp=True))
    (ROOT / "index-jp.html").write_text(html_ja, encoding="utf-8")

    print(f"Published EN chapters: {len(en_chaps)} (including EX)")
    print(f"Published JP chapters: {len(ja_chaps)} (including EX)")

if __name__ == "__main__":
    main()
