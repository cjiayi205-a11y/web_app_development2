from flask import Blueprint

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def list_categories():
    """
    分類列表頁面。
    邏輯: 取得所有分類資料。
    輸出: 渲染 categories/index.html
    """
    pass

@category_bp.route('/', methods=['POST'])
def create_category():
    """
    建立自訂分類。
    輸入: 表單資料 (name, type)
    邏輯: 存入資料庫。
    輸出: 重導向至分類列表
    """
    pass

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """
    刪除自訂分類。
    邏輯: 檢查是否為預設分類，若否則刪除。
    輸出: 重導向至分類列表
    """
    pass
