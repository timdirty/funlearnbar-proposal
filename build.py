#!/usr/bin/env python3
"""
樂程坊 AI × STEAM 課程提案產生器（公版系統）
=============================================
同一份 HTML 模板，換 config.json 就產出不同學校的提案。

使用方式:
  python3 build.py                              # 用 config.json
  python3 build.py --school "新學校" --dept "國中部"  # 覆蓋學校名
  python3 build.py --config other_school.json    # 指定不同 config
  python3 build.py --out output/proposal.html    # 指定輸出路徑（不覆蓋模板）

公版流程:
  1. admin.html 編輯 → 匯出 config.json
  2. python3 build.py --config XX.json --out docs/XX.html
  3. 部署到 GitHub Pages

後端 API 模式（未來）:
  config = requests.get('https://api.funlearnbar.com/v1/proposal/學校ID').json()
"""

import json, os, sys, re, shutil
from datetime import datetime

TEMPLATE = "docs/index.html"
BACKUP_DIR = "backups"

# 模板中的預設值（會被 config 覆蓋）
DEFAULTS = {
    'school': '再興幼兒園',
    'dept': '國小部',
    'title': '再興 AI × STEAM 課程總覽',
}


def load_config(path):
    if not os.path.exists(path):
        print(f"✗ {path} not found.")
        print(f"  請從 admin.html 匯出 JSON，或手動編輯")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    required = ['brand', 'target', 'courses']
    missing = [k for k in required if k not in data]
    if missing:
        print(f"✗ config 缺少必要欄位: {', '.join(missing)}")
        sys.exit(1)
    return data


def backup(filepath):
    if not os.path.exists(filepath):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.basename(filepath).replace('.html', '')
    dst = os.path.join(BACKUP_DIR, f"{name}_{ts}.html")
    shutil.copy2(filepath, dst)
    print(f"  📦 Backup: {dst}")


def build(config, school_override=None, dept_override=None):
    if not os.path.exists(TEMPLATE):
        print(f"✗ Template not found: {TEMPLATE}")
        return None

    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        html = f.read()

    t = config.get('target', {})
    school = school_override or t.get('school', '學校')
    dept = dept_override or t.get('dept', '')
    brand = config.get('brand', {}).get('name', '樂程坊')
    slogan = config.get('brand', {}).get('slogan', '')
    hero = config.get('hero', {})
    contact = config.get('contact', {})
    courses = [c for c in config.get('courses', []) if c.get('on', True)]
    recs = config.get('recs', [])

    print(f"\n  🏫 Target: {school} {dept}")
    print(f"  📚 Courses: {len(courses)} active")
    print(f"  🏆 Records: {len(recs)}")
    if contact:
        print(f"  📧 Contact: {contact.get('email','-')} | LINE {contact.get('line','-')}")

    # ── School name replacement ──
    if school != DEFAULTS['school']:
        html = html.replace(DEFAULTS['school'], school)
    if dept and dept != DEFAULTS['dept']:
        html = html.replace(DEFAULTS['dept'], dept)

    # ── Title + Meta ──
    new_title = f"{brand} — {school} AI × STEAM 課程總覽"
    html = html.replace(f"樂程坊 — {DEFAULTS['title']}", new_title)
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{new_title}">',
        html
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{brand} — 為{school}{dept}量身規劃的 AI × STEAM 科技課程提案。涵蓋 {len(courses)} 門課程、{len(recs)} 項競賽實績。">',
        html
    )

    # ── Embed config.json inline for config engine ──
    config_json = json.dumps(config, ensure_ascii=False, separators=(',',':'))
    # Inject as a global variable so config engine doesn't need to fetch
    inline_config = f'\n<script>window.__PROPOSAL_CONFIG__={config_json};</script>'
    html = html.replace('</head>', f'{inline_config}\n</head>')

    # ── Build timestamp ──
    ts = f'<!-- Built: {datetime.now().isoformat()} | {school} {dept} | {len(courses)} courses -->'
    html = html.replace('</head>', f'{ts}\n</head>')

    return html


def main():
    print("=" * 50)
    print("  樂程坊 AI × STEAM 提案產生器（公版）")
    print("=" * 50)

    config_path = "config.json"
    output_path = None
    school_override = None
    dept_override = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--school" and i + 1 < len(args):
            school_override = args[i + 1]; i += 2
        elif args[i] == "--dept" and i + 1 < len(args):
            dept_override = args[i + 1]; i += 2
        elif args[i] == "--config" and i + 1 < len(args):
            config_path = args[i + 1]; i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            output_path = args[i + 1]; i += 2
        elif args[i] in ("-h", "--help"):
            print("\n使用方式:")
            print("  python3 build.py                                # 用 config.json，覆蓋模板")
            print('  python3 build.py --school "新學校" --dept "國中部"   # 覆蓋學校名')
            print('  python3 build.py --config XX.json                # 指定不同 config')
            print('  python3 build.py --out output/proposal.html      # 輸出到其他路徑')
            print("\n公版流程:")
            print("  1. admin.html 匯出 config.json")
            print("  2. python3 build.py --config 新學校.json --out docs/新學校.html")
            print("  3. git push 部署")
            sys.exit(0)
        else:
            i += 1

    config = load_config(config_path)

    # Determine output
    final_output = output_path or TEMPLATE
    if os.path.exists(final_output):
        backup(final_output)

    html = build(config, school_override, dept_override)
    if html:
        os.makedirs(os.path.dirname(final_output) or '.', exist_ok=True)
        with open(final_output, 'w', encoding='utf-8') as f:
            f.write(html)
        size = os.path.getsize(final_output)
        print(f"\n  ✓ Generated: {final_output}")
        print(f"  📄 Size: {size:,} bytes ({size/1024:.0f} KB)")
        if output_path:
            print(f"\n  模板未被覆蓋，輸出到: {final_output}")
        print(f"\n  下一步: git add {final_output} && git commit && git push")
    else:
        print("\n  ✗ Build failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
