# 樂程坊 STEAM 課程提案系統

> 線上預覽: `https://你的帳號.github.io/funlearnbar-proposal/`

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
│   └── index.html      ← GitHub Pages 入口（提案網頁）
├── admin.jsx            ← CMS 管理後台（在 Claude.ai 開啟）
├── config.json          ← 資料結構定義
├── build.py             ← 靜態網頁產生器
└── README.md            ← 本文件
```

## 系統架構

```
admin.jsx (CMS 後台)  →  config.json  →  build.py  →  docs/index.html
     ↕                                                      ↓
window.storage (DB)                                   GitHub Pages
```

### 換學校流程
1. 在 Claude.ai 開啟 `admin.jsx` 編輯
2. 匯出 `config.json`
3. 執行 `python3 build.py` 產生新的 `docs/index.html`
4. Push 到 GitHub 自動更新

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
