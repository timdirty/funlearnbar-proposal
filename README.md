# 樂程坊 STEAM 課程提案系統

> 提案網頁: https://timdirty.github.io/funlearnbar-proposal/
> 管理後台: https://timdirty.github.io/funlearnbar-proposal/admin.html

## 檔案結構

```
funlearnbar-proposal/
├── docs/
│   ├── index.html       ← 提案網頁（GitHub Pages 入口）
│   ├── admin.html       ← CMS 管理後台（瀏覽器直接操作）
│   └── 404.html         ← 自訂 404 頁面
├── admin.jsx            ← CMS 原始碼（Claude.ai Artifact 版）
├── config.json          ← 資料結構定義
├── build.py             ← 換學校產生器
├── .gitignore
└── README.md
```

## 系統架構

```
docs/admin.html (CMS 後台)  →  匯出 config.json  →  build.py  →  docs/index.html
       ↕                                                              ↓
  localStorage (DB)                                             GitHub Pages
```

## 管理後台功能

開啟 [admin.html](https://timdirty.github.io/funlearnbar-proposal/admin.html) 即可操作：

| Tab | 功能 |
|-----|------|
| 即時預覽 | 提案卡片完整預覽 |
| 學校設定 | 學校名稱、品牌、Hero 標語、四大亮點 |
| 課程管理 | 11 門課程 CRUD、開關切換、路線/學段分類 |
| 競賽戰績 | 三個時期、13 筆成績紀錄管理 |

- 支援多校管理（頂部切換）
- JSON 匯出 / 匯入
- 自動儲存至 localStorage
- 手機響應式（底部 Tab Bar）
- 刪除操作有確認對話框

## 換學校（build.py）

```bash
# 方法 1：用 config.json 設定
python3 build.py

# 方法 2：命令列覆蓋
python3 build.py --school "新學校" --dept "國中部"

# 說明
python3 build.py --help
```

會自動備份舊版 index.html 到 `backups/`，然後替換學校名稱、meta 標籤等。

## 提案網頁規格

| 項目 | 規格 |
|------|------|
| 課程 | 3 路線 × 4 學段 = 11 門 |
| 競賽 | 13 項對接 + 歷年戰績 |
| 圖片 | 14 張 base64 內嵌 |
| 響應式 | 320px — 1440px |
| SEO | Open Graph + meta description |
| 無障礙 | skip-to-content / focus-visible / reduced-motion |
| 觸控 | hover:none 專屬優化 |
| 列印 | @media print 最佳化 |
