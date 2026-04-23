def register_blueprints(app):
    """
    註冊所有的 Flask Blueprints 到主要的 app 中。
    """
    from .main import main_bp
    from .expense import expense_bp
    from .category import category_bp
    from .report import report_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(report_bp)
