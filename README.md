# 樂程坊 STEAM 課程提案系統

> 提案網頁: https://timdirty.github.io/funlearnbar-proposal/
> 管理後台: https://timdirty.github.io/funlearnbar-proposal/admin.html

## 發布到 GitHub Pages（3 分鐘）

### Step 1 — 建立 Repository
1. 打開 [github.com/new](https://github.com/new)
2. Repository name 填 `funlearnbar-proposal`
3. 選 **Public**
4. 點 **Create repository**

### Step 2 — 上傳檔案
1. 在新建的 repo 頁面點 **uploading an existing file**
2. 把下載的 zip 解壓縮
3. 把 **所有檔案和 `docs` 資料夾** 拖進上傳區
4. 點 **Commit changes**

### Step 3 — 啟用 GitHub Pages
1. 進入 repo → **Settings** → 左側 **Pages**
2. Source 選 **Deploy from a branch**
3. Branch 選 `main`，資料夾選 `/docs`
4. 點 **Save**
5. 等 1-2 分鐘，頁面上方會出現公開網址

---

## 檔案結構

```
funlearnbar-proposal/
├── docs/
│   ├── index.html       ← 提案網頁（GitHub Pages 入口）
│   └── admin.html       ← CMS 管理後台（瀏覽器直接操作）
├── admin.jsx            ← CMS 原始碼（Claude.ai Artifact 版）
├── config.json          ← 資料結構定義
├── build.py             ← 靜態網頁產生器
└── README.md            ← 本文件
```

## 系統架構

```
docs/admin.html (CMS 後台)  →  匯出 config.json  →  build.py  →  docs/index.html
       ↕                                                              ↓
  localStorage (DB)                                             GitHub Pages
```

### 管理後台使用方式
1. 開啟 https://timdirty.github.io/funlearnbar-proposal/admin.html
2. 在「學校設定」修改學校名稱、品牌資訊
3. 在「課程管理」新增 / 編輯 / 開關課程
4. 在「競賽戰績」管理歷年成績
5. 點「⬇ JSON」匯出 `config.json`
6. 資料自動存在瀏覽器 localStorage，重新整理不會遺失

### 接後端 API
```python
config = requests.get('https://api.example.com/proposal/學校名').json()
html = build(config)
```

## 提案網頁規格

| 項目 | 規格 |
|------|------|
| 課程 | 3 路線 x 4 學段 = 11 門 |
| 競賽 | 13 項對接 + 21 筆歷年戰績 |
| 圖片 | 14 張 base64 內嵌 |
| 響應式 | 320px - 1440px |
| 觸控 | hover:none 專屬優化 |
| 無障礙 | focus-visible / reduced-motion |
