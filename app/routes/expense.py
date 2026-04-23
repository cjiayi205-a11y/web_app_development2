from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.expense import ExpenseModel
from app.models.category import CategoryModel

expense_bp = Blueprint('expense', __name__, url_prefix='/expenses')

@expense_bp.route('/')
def list_expenses():
    """
    收支明細列表。
    輸入: ?month=YYYY-MM (可選)
    邏輯: 取得篩選條件下的所有收支明細。
    輸出: 渲染 expenses/index.html
    """
    month = request.args.get('month', '')
    expenses = ExpenseModel.get_all(month=month if month else None)
    return render_template('expenses/index.html', expenses=expenses, current_month=month)

@expense_bp.route('/new', methods=['GET'])
def new_expense():
    """
    新增收支表單頁面。
    邏輯: 取得分類列表供選單使用。
    輸出: 渲染 expenses/new.html
    """
    categories = CategoryModel.get_all()
    return render_template('expenses/new.html', categories=categories)

@expense_bp.route('/', methods=['POST'])
def create_expense():
    """
    建立收支紀錄。
    輸入: 表單資料 (amount, record_date, category_id, note)
    邏輯: 驗證資料並存入資料庫。
    輸出: 重導向至首頁或列表頁
    """
    amount = request.form.get('amount')
    record_date = request.form.get('record_date')
    category_id = request.form.get('category_id')
    note = request.form.get('note', '')

    if not amount or not record_date or not category_id:
        flash('請填寫所有必填欄位 (金額、日期、分類)', 'danger')
        return redirect(url_for('expense.new_expense'))

    try:
        amount = float(amount)
        ExpenseModel.create(amount, record_date, note, int(category_id))
        flash('成功新增收支紀錄', 'success')
    except ValueError:
        flash('金額格式錯誤', 'danger')
        return redirect(url_for('expense.new_expense'))

    return redirect(url_for('main.index'))

@expense_bp.route('/<int:id>/edit', methods=['GET'])
def edit_expense(id):
    """
    編輯收支表單頁面。
    邏輯: 取得單筆收支與分類列表。
    輸出: 渲染 expenses/edit.html
    """
    expense = ExpenseModel.get_by_id(id)
    if not expense:
        flash('找不到該筆紀錄', 'danger')
        return redirect(url_for('expense.list_expenses'))
        
    categories = CategoryModel.get_all()
    return render_template('expenses/edit.html', expense=expense, categories=categories)

@expense_bp.route('/<int:id>/update', methods=['POST'])
def update_expense(id):
    """
    更新收支紀錄。
    輸入: 表單資料
    邏輯: 驗證並更新資料庫。
    輸出: 重導向至列表頁
    """
    amount = request.form.get('amount')
    record_date = request.form.get('record_date')
    category_id = request.form.get('category_id')
    note = request.form.get('note', '')

    if not amount or not record_date or not category_id:
        flash('請填寫所有必填欄位', 'danger')
        return redirect(url_for('expense.edit_expense', id=id))

    try:
        ExpenseModel.update(id, float(amount), record_date, note, int(category_id))
        flash('收支紀錄更新成功', 'success')
    except ValueError:
        flash('金額格式錯誤', 'danger')
        return redirect(url_for('expense.edit_expense', id=id))

    return redirect(url_for('expense.list_expenses'))

@expense_bp.route('/<int:id>/delete', methods=['POST'])
def delete_expense(id):
    """
    刪除收支紀錄。
    邏輯: 從資料庫中刪除該筆紀錄。
    輸出: 重導向至列表頁
    """
    ExpenseModel.delete(id)
    flash('收支紀錄已刪除', 'success')
    return redirect(url_for('expense.list_expenses'))
