from flask import Blueprint, render_template, request, flash
from datetime import datetime
from app.models.expense import ExpenseModel
from app.models.budget import BudgetModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示當月總覽、餘額與近期收支。
    輸入: ?month=YYYY-MM (可選)
    邏輯: 取得當月收支與預算進度，計算餘額。
    輸出: 渲染 index.html
    """
    # 取得月份參數，預設為當前月份
    current_month = datetime.now().strftime('%Y-%m')
    month = request.args.get('month', current_month)
    
    # 取得當月所有收支
    expenses = ExpenseModel.get_all(month=month)
    
    # 取得當月預算
    budget = BudgetModel.get_by_month(month)
    budget_amount = budget['amount'] if budget else 0
    
    # 計算總收入與總支出
    total_income = sum(e['amount'] for e in expenses if e['category_type'] == 'income')
    total_expense = sum(e['amount'] for e in expenses if e['category_type'] == 'expense')
    balance = total_income - total_expense
    
    return render_template(
        'index.html', 
        month=month,
        expenses=expenses[:5], # 首頁只顯示最近 5 筆
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        budget_amount=budget_amount
    )
