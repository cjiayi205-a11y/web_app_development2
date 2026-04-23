from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示當月總覽、餘額與近期收支。
    輸入: ?month=YYYY-MM (可選)
    邏輯: 取得當月收支與預算進度，計算餘額。
    輸出: 渲染 index.html
    """
    pass
