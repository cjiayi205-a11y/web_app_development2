from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.category import CategoryModel

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def list_categories():
    """
    分類列表頁面。
    邏輯: 取得所有分類資料。
    輸出: 渲染 categories/index.html
    """
    categories = CategoryModel.get_all()
    return render_template('categories/index.html', categories=categories)

@category_bp.route('/', methods=['POST'])
def create_category():
    """
    建立自訂分類。
    輸入: 表單資料 (name, type)
    邏輯: 存入資料庫。
    輸出: 重導向至分類列表
    """
    name = request.form.get('name')
    cat_type = request.form.get('type')
    
    if not name or not cat_type:
        flash('分類名稱與類型為必填', 'danger')
        return redirect(url_for('category.list_categories'))
        
    if cat_type not in ['income', 'expense']:
        flash('類型必須為 income 或 expense', 'danger')
        return redirect(url_for('category.list_categories'))
        
    CategoryModel.create(name, cat_type)
    flash('自訂分類建立成功', 'success')
    return redirect(url_for('category.list_categories'))

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """
    刪除自訂分類。
    邏輯: 檢查是否為預設分類，若否則刪除。
    輸出: 重導向至分類列表
    """
    cat = CategoryModel.get_by_id(id)
    if not cat:
        flash('找不到該分類', 'danger')
    elif cat['is_default']:
        flash('系統預設分類不可刪除', 'danger')
    else:
        success = CategoryModel.delete(id)
        if success:
            flash('分類刪除成功', 'success')
        else:
            flash('刪除失敗', 'danger')
            
    return redirect(url_for('category.list_categories'))
