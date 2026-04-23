from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models.expense import ExpenseModel
from app.models.budget import BudgetModel

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['GET'])
def view_report():
    """
    報表分析頁面。
    輸入: ?month=YYYY-MM (可選)
    邏輯: 依據分類統計當月支出金額，準備供圖表渲染的資料。
    輸出: 渲染 report/index.html
    """
    current_month = datetime.now().strftime('%Y-%m')
    month = request.args.get('month', current_month)
    
    expenses = ExpenseModel.get_all(month=month)
    
    # 統計各分類的支出總額
    expense_data = {}
    for e in expenses:
        if e['category_type'] == 'expense':
            cat_name = e['category_name']
            expense_data[cat_name] = expense_data.get(cat_name, 0) + e['amount']
            
    labels = list(expense_data.keys())
    values = list(expense_data.values())
    
    return render_template('report/index.html', month=month, labels=labels, values=values)

@report_bp.route('/budget', methods=['POST'])
def set_budget():
    """
    設定或更新預算。
    輸入: 表單資料 (month, amount)
    邏輯: 儲存或更新至資料庫。
    輸出: 重導向回上一頁
    """
    month = request.form.get('month')
    amount = request.form.get('amount')
    
    if not month or not amount:
        flash('月份與預算金額為必填', 'danger')
        return redirect(request.referrer or url_for('main.index'))
        
    try:
        amount = float(amount)
        BudgetModel.set_budget(month, amount)
        flash(f'{month} 預算設定成功', 'success')
    except ValueError:
        flash('預算金額格式錯誤', 'danger')
        
    return redirect(request.referrer or url_for('main.index'))
