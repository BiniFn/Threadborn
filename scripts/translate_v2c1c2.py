import os
import re
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

# Initialize translator
translator = GoogleTranslator(source='en', target='ja')

def batch_translate_single(texts):
    res = []
    for t in texts:
        if not t.strip():
            res.append(t)
        else:
            try:
                translated = translator.translate(t.strip())
                prefix = t[:len(t) - len(t.lstrip())]
                suffix = t[len(t.rstrip()):]
                res.append(prefix + translated + suffix)
            except:
                res.append(t)
    return res

def translate_html_content(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')
    texts_to_translate = []
    nodes = []
    
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            continue
        text = text_node.string
        if text and text.strip() and not text.strip() == '&nbsp;':
            texts_to_translate.append(text)
            nodes.append(text_node)
            
    translated_texts = batch_translate_single(texts_to_translate) 
    
    for node, tr_text in zip(nodes, translated_texts):
        node.replace_with(NavigableString(tr_text))
        
    return str(soup)

def process_file(filepath):
    print(f"Translating V2C1 and V2C2 in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    chapters_start = content.find('const chapters = [')
    characters_start = content.find('const characters = [')
    
    chapters_block = content[chapters_start:characters_start]
    
    # Let's find Volume 2 Chapter 1 & 2 objects.
    # They are in the chapters_block.
    # We will use regex to find the `pages:` array for each of them and translate only those strings.
    # We can also translate the title, label, summary!
    
    def translate_obj(match):
        block = match.group(0)
        # translate title
        def tr_title(m):
            return 'title: "' + translator.translate(m.group(1)) + '"'
        block = re.sub(r'title:\s*"([^"]+)"', tr_title, block)
        
        # translate label
        def tr_label(m):
            return 'label: "' + translator.translate(m.group(1)) + '"'
        block = re.sub(r'label:\s*"([^"]+)"', tr_label, block)
        
        # translate summary
        def tr_summary(m):
            return 'summary: "' + translator.translate(m.group(1)) + '"'
        block = re.sub(r'summary:\s*"([^"]+)"', tr_summary, block)

        # translate pages
        def tr_pages(m):
            html = m.group(1)
            translated = translate_html_content(html)
            return f'`{translated}`'
        block = re.sub(r'`(.*?)`', tr_pages, block, flags=re.DOTALL)

        return block
        
    # V2C1 block starts with: volume: "Volume 2", \n chapter: "Chapter 1"
    # and ends before volume: "Volume 2", \n chapter: "Chapter 2"
    v2c1_regex = r'\{\s*volume:\s*"Volume 2",\s*chapter:\s*"Chapter 1".*?(?=\{\s*volume:\s*"Volume 2",\s*chapter:\s*"Chapter 2")'
    chapters_block = re.sub(v2c1_regex, translate_obj, chapters_block, flags=re.DOTALL)
    
    v2c2_regex = r'\{\s*volume:\s*"Volume 2",\s*chapter:\s*"Chapter 2".*?(?=\{\s*volume:\s*"Volume 2",\s*chapter:\s*"Chapter 3")'
    chapters_block = re.sub(v2c2_regex, translate_obj, chapters_block, flags=re.DOTALL)

    content = content[:chapters_start] + chapters_block + content[characters_start:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Done!")

process_file('/Users/amela/Downloads/Threadborn-Starting-Life-Beyond-the-Covenant-Door/index-jp.html')
