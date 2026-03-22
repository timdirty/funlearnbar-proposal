#!/usr/bin/env python3
"""
樂程坊 STEAM 課程提案產生器
==============================
公版模板 — 換學校只改 config.json，跑一次就產出完整提案網頁。

使用方式:
  1. 從 admin.jsx 管理後台匯出 config.json
  2. 將 Logo 放在 images/logo.jpg
  3. 將課程圖片放在 images/01.jpg ~ images/11.jpg
  4. 執行: python3 build.py
  5. 產出: output/proposal.html

接後端 API:
  config = requests.get('https://api.funlearnbar.com/proposal/再興').json()
  generate(config, images)
"""

import json, base64, os, sys, re
from pathlib import Path
from datetime import datetime

CONFIG = "config.json"
IMAGES = "images"
OUTPUT = "output/proposal.html"
TEMPLATE = "proposal.html"  # Use existing HTML as template

def load_config():
    if not os.path.exists(CONFIG):
        print(f"✗ {CONFIG} not found. Export from admin.jsx first.")
        sys.exit(1)
    with open(CONFIG, 'r', encoding='utf-8') as f:
        return json.load(f)

def encode_image(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'rb') as f:
        data = f.read()
    ext = Path(path).suffix.lower()
    mime = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}.get(ext, 'image/jpeg')
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

def build(config, template_path=TEMPLATE):
    """Replace target school info in existing template"""
    if not os.path.exists(template_path):
        print(f"✗ Template {template_path} not found")
        return None
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    t = config.get('target', {})
    school = t.get('school', '學校')
    dept = t.get('dept', '')
    
    print(f"  Target: {school} {dept}")
    print(f"  Courses: {len([c for c in config.get('courses', []) if c.get('on', True)])}")
    print(f"  Records: {len(config.get('recs', []))}")
    
    # Replace school-specific text
    html = html.replace('再興幼兒園', school)
    if dept:
        html = html.replace('國小部', dept)
    
    # Add build timestamp
    html = html.replace('</head>', f'<!-- Built: {datetime.now().isoformat()} for {school} {dept} -->\n</head>')
    
    return html

def main():
    print("=" * 50)
    print("樂程坊 STEAM 課程提案產生器")
    print("=" * 50)
    
    config = load_config()
    
    os.makedirs("output", exist_ok=True)
    
    html = build(config)
    if html:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n✓ Generated: {OUTPUT}")
        print(f"  Size: {os.path.getsize(OUTPUT):,} bytes")
    
    print(f"\n要接後端 API：")
    print(f"  config = requests.get('https://api.funlearnbar.com/proposal/學校').json()")
    print(f"  html = build(config)")

if __name__ == "__main__":
    main()
