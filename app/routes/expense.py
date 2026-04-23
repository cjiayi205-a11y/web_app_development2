from flask import Blueprint

expense_bp = Blueprint('expense', __name__, url_prefix='/expenses')

@expense_bp.route('/')
def list_expenses():
    """
    收支明細列表。
    輸入: ?month=YYYY-MM (可選)
    邏輯: 取得篩選條件下的所有收支明細。
    輸出: 渲染 expenses/index.html
    """
    pass

@expense_bp.route('/new', methods=['GET'])
def new_expense():
    """
    新增收支表單頁面。
    邏輯: 取得分類列表供選單使用。
    輸出: 渲染 expenses/new.html
    """
    pass

@expense_bp.route('/', methods=['POST'])
def create_expense():
    """
    建立收支紀錄。
    輸入: 表單資料 (amount, record_date, category_id, note)
    邏輯: 驗證資料並存入資料庫。
    輸出: 重導向至首頁或列表頁
    """
    pass

@expense_bp.route('/<int:id>/edit', methods=['GET'])
def edit_expense(id):
    """
    編輯收支表單頁面。
    邏輯: 取得單筆收支與分類列表。
    輸出: 渲染 expenses/edit.html
    """
    pass

@expense_bp.route('/<int:id>/update', methods=['POST'])
def update_expense(id):
    """
    更新收支紀錄。
    輸入: 表單資料
    邏輯: 驗證並更新資料庫。
    輸出: 重導向至列表頁
    """
    pass

@expense_bp.route('/<int:id>/delete', methods=['POST'])
def delete_expense(id):
    """
    刪除收支紀錄。
    邏輯: 從資料庫中刪除該筆紀錄。
    輸出: 重導向至列表頁
    """
    pass
