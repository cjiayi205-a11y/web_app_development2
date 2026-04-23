# 路由設計文件 (Routes Design) - 個人記帳簿

本文件定義了「個人記帳簿」系統的所有路由路徑、HTTP 方法以及對應的處理邏輯與渲染模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 (總覽) | GET | `/` | `index.html` | 顯示當月餘額、近期收支與預算進度 |
| 收支列表 | GET | `/expenses/` | `expenses/index.html` | 顯示所有收支明細，支援月份篩選 |
| 新增收支頁面 | GET | `/expenses/new` | `expenses/new.html` | 顯示新增收支表單 |
| 建立收支 | POST | `/expenses/` | — | 接收表單，存入 DB，重導向至列表或首頁 |
| 編輯收支頁面 | GET | `/expenses/<id>/edit` | `expenses/edit.html` | 顯示特定收支的編輯表單 |
| 更新收支 | POST | `/expenses/<id>/update` | — | 接收表單，更新 DB，重導向至列表 |
| 刪除收支 | POST | `/expenses/<id>/delete` | — | 刪除收支，重導向至列表 |
| 分類列表 | GET | `/categories/` | `categories/index.html` | 顯示所有分類 |
| 建立分類 | POST | `/categories/` | — | 接收表單，存入 DB，重導向至分類列表 |
| 刪除分類 | POST | `/categories/<id>/delete` | — | 刪除自訂分類，重導向至分類列表 |
| 報表分析 | GET | `/report` | `report/index.html` | 顯示當月支出比例的圖表 |
| 設定預算 | POST | `/budget` | — | 更新當月預算，重導向回上一頁 |

## 2. 每個路由的詳細說明

### 2.1 首頁 `/` (GET)
- **輸入**: 可選 Query String `month` (例如 `?month=2026-04`)
- **處理邏輯**: 
  - 呼叫 `ExpenseModel.get_all(month)` 取得該月收支
  - 呼叫 `BudgetModel.get_by_month(month)` 取得該月預算
  - 計算總收入、總支出與當前餘額
- **輸出**: 渲染 `index.html`
- **錯誤處理**: 無特殊錯誤，若無資料則各項數據顯示為 0

### 2.2 收支相關 (Expense)
- **`/expenses/` (GET)**: 
  - 邏輯: 取得特定月份的明細，渲染 `expenses/index.html`
- **`/expenses/new` (GET)**:
  - 邏輯: 呼叫 `CategoryModel.get_all()` 取得選單，渲染 `expenses/new.html`
- **`/expenses/` (POST)**:
  - 輸入: 表單 `amount`, `record_date`, `category_id`, `note`
  - 邏輯: 驗證必填，呼叫 `ExpenseModel.create()`
  - 輸出: `redirect('/')` 或 `redirect('/expenses/')`
- **`/expenses/<id>/edit` (GET)**:
  - 邏輯: 取得特定 ID 收支與分類清單，渲染 `expenses/edit.html`
  - 錯誤: 若找不到該 ID 回傳 404
- **`/expenses/<id>/update` (POST)**:
  - 邏輯: 呼叫 `ExpenseModel.update()`
  - 輸出: `redirect('/expenses/')`
- **`/expenses/<id>/delete` (POST)**:
  - 邏輯: `ExpenseModel.delete()`
  - 輸出: `redirect('/expenses/')`

### 2.3 分類相關 (Category)
- **`/categories/` (GET)**: 顯示分類清單（包含新增表單區塊），渲染 `categories/index.html`
- **`/categories/` (POST)**: 接收表單，呼叫 `CategoryModel.create()`，成功後 `redirect('/categories/')`
- **`/categories/<id>/delete` (POST)**: 檢查是否為內建預設，若否則刪除並 `redirect('/categories/')`

### 2.4 報表與預算 (Report & Budget)
- **`/report` (GET)**: 
  - 邏輯: 依據分類統計當月金額，組合出 Chart.js 需要的 JSON 結構
  - 輸出: 渲染 `report/index.html`
- **`/budget` (POST)**:
  - 輸入: `month`, `amount`
  - 邏輯: `BudgetModel.set_budget()`
  - 輸出: 返回推薦頁面

## 3. Jinja2 模板清單

所有的 HTML 檔案皆繼承自共用框架 `base.html`：
- `templates/base.html`：導覽列、頁尾、CSS/JS 引入
- `templates/index.html`：儀表板
- `templates/expenses/index.html`：明細列表
- `templates/expenses/new.html`：新增收支
- `templates/expenses/edit.html`：編輯收支
- `templates/categories/index.html`：分類管理
- `templates/report/index.html`：圖表報表

## 4. 路由骨架程式碼
所有對應的路由骨架（含 Blueprint 與 Docstring）已建立於 `app/routes/` 目錄中。
