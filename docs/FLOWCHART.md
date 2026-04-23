# 流程圖文件 (Flowchart) - 個人記帳簿

本文件旨在視覺化「個人記帳簿」系統的使用者操作路徑與系統資料流動流程，幫助團隊在開發階段建立一致的認知。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者進入系統後的主要操作路徑，包含瀏覽首頁、新增收支、管理分類與檢視報表等。

```mermaid
flowchart LR
    A([使用者進入網站]) --> B[首頁 - 總覽儀表板]
    
    B --> C{選擇操作}
    
    C -->|查看明細| D[收支明細列表頁]
    D --> E[篩選月份/分類]
    D --> F[編輯/刪除特定紀錄]
    
    C -->|新增紀錄| G[新增收支表單頁]
    G --> H{填寫表單}
    H -->|提交| I[儲存並返回首頁/列表]
    H -->|取消| B
    
    C -->|管理分類| J[分類設定頁]
    J --> K[新增/編輯/刪除自訂分類]
    
    C -->|設定預算| L[預算設定頁]
    L --> M[更新當月預算]
    
    C -->|查看報表| N[報表分析頁]
    N --> O[查看圓餅圖/長條圖趨勢]
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述了使用者在「新增收支紀錄」時，系統各元件（前端瀏覽器、Flask 後端、SQLite 資料庫）之間的互動時序與資料流。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Route as Flask Route (控制器)
    participant Model as Model (資料模型)
    participant DB as SQLite (資料庫)
    
    User->>Browser: 1. 點擊「新增收支」按鈕
    Browser->>Route: 2. GET /expenses/new
    Route-->>Browser: 3. 回傳包含分類選單的 HTML 表單
    User->>Browser: 4. 填寫金額、分類、日期等資料並送出
    Browser->>Route: 5. POST /expenses 帶有表單資料
    
    rect rgb(240, 248, 255)
        Note right of Route: 後端驗證與儲存
        Route->>Model: 6. 呼叫新增收支的邏輯
        Model->>DB: 7. 執行 INSERT INTO SQL 指令
        DB-->>Model: 8. 回傳寫入成功
        Model-->>Route: 9. 處理完畢
    end
    
    Route-->>Browser: 10. 回傳 302 Redirect (重導向至首頁或明細頁)
    Browser->>User: 11. 重新載入頁面，顯示最新收支與餘額
```

## 3. 功能清單與路由對照表

以下整理了系統主要功能所對應的 URL 路徑與 HTTP 請求方法，可供後續 API 與路由設計參考：

| 功能模組 | 功能描述 | URL 路徑 | HTTP 方法 | 備註 |
|---|---|---|---|---|
| **首頁總覽 (Home)** | 顯示當月餘額、近期收支與預算進度 | `/` | GET | 渲染 `index.html` |
| **收支管理 (Expense)** | 瀏覽所有收支明細（可加上條件過濾） | `/expenses` | GET | |
| | 顯示新增收支表單頁面 | `/expenses/new` | GET | |
| | 提交新增的收支資料 | `/expenses` | POST | 成功後重導向 |
| | 顯示編輯特定收支表單頁面 | `/expenses/<id>/edit` | GET | |
| | 提交編輯後的收支資料 | `/expenses/<id>` | POST | |
| | 刪除特定收支紀錄 | `/expenses/<id>/delete` | POST | |
| **分類管理 (Category)** | 瀏覽分類列表與新增表單 | `/categories` | GET | |
| | 提交新增分類資料 | `/categories` | POST | |
| | 刪除特定自訂分類 | `/categories/<id>/delete` | POST | |
| **報表與預算 (Report)** | 查看圖表分析（圓餅圖等） | `/report` | GET | |
| | 提交並更新當月預算設定 | `/budget` | POST | 可在總覽頁操作 |
