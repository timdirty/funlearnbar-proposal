#!/usr/bin/env python3
"""
樂程坊 STEAM 課程提案產生器
==============================
換學校只改 config.json，跑一次就產出新的提案網頁。

使用方式:
  1. 從 admin.html 管理後台匯出 config.json
  2. 執行: python3 build.py
  3. 產出: docs/index.html（自動覆蓋）

換學校:
  python3 build.py --school "新學校" --dept "國中部"
"""

import json, os, sys, re, shutil
from datetime import datetime

CONFIG = "config.json"
TEMPLATE = "docs/index.html"
OUTPUT = "docs/index.html"
BACKUP_DIR = "backups"

# 預設替換對照（index.html 中硬編碼的文字）
DEFAULT_SCHOOL = "再興幼兒園"
DEFAULT_DEPT = "國小部"
DEFAULT_TITLE = "再興 STEAM 課程總覽"


def load_config():
    if not os.path.exists(CONFIG):
        print(f"✗ {CONFIG} not found.")
        print(f"  請從 admin.html 匯出 JSON，或手動編輯 config.json")
        sys.exit(1)
    with open(CONFIG, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 基本驗證
    required = ['brand', 'target', 'courses']
    missing = [k for k in required if k not in data]
    if missing:
        print(f"✗ config.json 缺少必要欄位: {', '.join(missing)}")
        sys.exit(1)
    return data


def backup_template():
    """備份目前的 index.html"""
    if not os.path.exists(TEMPLATE):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(BACKUP_DIR, f"index_{ts}.html")
    shutil.copy2(TEMPLATE, dst)
    print(f"  📦 Backup: {dst}")


def build(config, school_override=None, dept_override=None):
    """讀取 docs/index.html 模板，替換學校資訊"""
    if not os.path.exists(TEMPLATE):
        print(f"✗ Template not found: {TEMPLATE}")
        return None

    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        html = f.read()

    t = config.get('target', {})
    school = school_override or t.get('school', '學校')
    dept = dept_override or t.get('dept', '')
    brand = config.get('brand', {}).get('name', '樂程坊')
    courses = [c for c in config.get('courses', []) if c.get('on', True)]
    recs = config.get('recs', [])

    print(f"\n  🏫 Target: {school} {dept}")
    print(f"  📚 Courses: {len(courses)} active")
    print(f"  🏆 Records: {len(recs)}")

    # 替換學校名稱
    if school != DEFAULT_SCHOOL:
        html = html.replace(DEFAULT_SCHOOL, school)

    # 替換部門
    if dept and dept != DEFAULT_DEPT:
        html = html.replace(DEFAULT_DEPT, dept)

    # 替換 title
    new_title = f"{brand} — {school} STEAM 課程總覽"
    html = html.replace(
        f"樂程坊 — {DEFAULT_TITLE}",
        new_title
    )

    # 更新 OG meta
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{new_title}">',
        html
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{brand} — 為{school}{dept}量身規劃的 STEAM 科技課程提案。涵蓋 {len(courses)} 門課程、{len(recs)} 項競賽實績。">',
        html
    )

    # 加入 build 時間戳
    ts_comment = f'<!-- Built: {datetime.now().isoformat()} | {school} {dept} | {len(courses)} courses, {len(recs)} records -->'
    html = html.replace('</head>', f'{ts_comment}\n</head>')

    return html


def main():
    print("=" * 50)
    print("  樂程坊 STEAM 課程提案產生器")
    print("=" * 50)

    # 解析命令列參數
    school_override = None
    dept_override = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--school" and i + 1 < len(args):
            school_override = args[i + 1]
            i += 2
        elif args[i] == "--dept" and i + 1 < len(args):
            dept_override = args[i + 1]
            i += 2
        elif args[i] in ("-h", "--help"):
            print("\n使用方式:")
            print("  python3 build.py                        # 用 config.json 設定")
            print('  python3 build.py --school "新學校"        # 覆蓋學校名')
            print('  python3 build.py --school "X" --dept "Y"  # 覆蓋學校+部門')
            sys.exit(0)
        else:
            i += 1

    config = load_config()

    # 備份
    backup_template()

    html = build(config, school_override, dept_override)
    if html:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write(html)
        size = os.path.getsize(OUTPUT)
        print(f"\n  ✓ Generated: {OUTPUT}")
        print(f"  📄 Size: {size:,} bytes ({size/1024:.0f} KB)")
        print(f"\n  下一步: git add docs/index.html && git commit && git push")
    else:
        print("\n  ✗ Build failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
