from flask import Blueprint

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['GET'])
def view_report():
    """
    報表分析頁面。
    輸入: ?month=YYYY-MM (可選)
    邏輯: 依據分類統計當月支出金額，準備供圖表渲染的資料。
    輸出: 渲染 report/index.html
    """
    pass

@report_bp.route('/budget', methods=['POST'])
def set_budget():
    """
    設定或更新預算。
    輸入: 表單資料 (month, amount)
    邏輯: 儲存或更新至資料庫。
    輸出: 重導向回上一頁
    """
    pass
