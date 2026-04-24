import re
import os

with open('chap4_raw.txt', 'r') as f:
    text = f.read()

# Find chapter 4 volume 2 content
part1 = "## Chapter 4: The One Who Collects Endings"
if part1 not in text:
    print("Could not find chapter 4 start")
    exit(1)

chapter4_text = text.split(part1)[1]
summary_text = chapter4_text.split("*In which ")[1].split("*")[0].strip()
summary_text = "In which " + summary_text

# the rest of the content is after the next "---"
content = chapter4_text.split("*In which ")[1].split("---", 1)[1].strip()

# Split content into pages/sections based on '---'
sections = [s.strip() for s in content.split('---')]

pages = []

# process inline markdown
def process_inline(text):
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text

for i, section in enumerate(sections):
    if not section.strip(): continue
    
    if i == 0:
        page_html = f"""          `<div class="chapter-head">
            <span class="chapter-num">Volume 02 · Chapter 04</span>
            <h2 class="chapter-title">The One Who Collects Endings</h2>
            <p class="chapter-subtitle">{process_inline(summary_text)}</p>
          </div>
          <div class="ep-intro-bar"><p>The Archivist · Divine Bloom · New Limits</p></div>"""
    else:
        page_html = "          `"
    
    # paragraphs
    lines = section.strip().split('\n\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith('### '):
            page_html += f'\n          <p class="scene-title">{process_inline(line[4:])}</p>'
        elif line.startswith('>'):
            box_content = line.replace(">", "").strip()
            # if multiple lines in blockquote
            box_lines = box_content.split('\n')
            final_box = "<br>".join([process_inline(l.strip().lstrip('>').strip()) for l in box_lines])
            page_html += f'\n          <div class="system-box">{final_box}</div>'
        elif line == '*— End of Chapter 04 —*':
            page_html += f'\n          <div class="tbc">— End of Chapter 04 —</div>'
        else:
            # Handle possible multiline strings
            line = line.replace('\n', '<br>')
            page_html += f'\n          <p class="novel-p">{process_inline(line)}</p>'
    
    page_html += "`"
    pages.append(page_html)

pages_str = ",\n".join(pages)

chapter_obj = f"""      {{
        volume: "Volume 2",
        chapter: "Chapter 4",
        label: "The One Who Collects Endings",
        title: "The One Who Collects Endings",
        summary: "Cadreth the Archivist arrives to file the end of the story, but Violet unleashes Bloom Absolute to ensure the record stays open.",
        tags: ["archivist", "bloom absolute", "divine class", "new ceiling"],
        pages: [
{pages_str}
        ]
      }}"""

# Insert into index.html
with open('index.html', 'r') as f:
    html = f.read()

if "The One Who Collects Endings" in html:
    print("Chapter 4 already in index.html")
    exit(0)

# We want to insert it at the end of the chapters array
html = html.replace('        ]\n      }\n    ];', '        ]\n      },\n' + chapter_obj + '\n    ];')

with open('index.html', 'w') as f:
    f.write(html)

print("Added Chapter 4 to index.html successfully")
