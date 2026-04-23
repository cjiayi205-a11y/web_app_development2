import os
from flask import Flask
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    # 初始化 Flask 應用程式
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'app', 'templates'),
                static_folder=os.path.join(base_dir, 'app', 'static'))
    
    # 設定應用程式
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 初始化資料庫 (確保 instance 資料夾與 table 存在)
    with app.app_context():
        from app.models.db import init_db
        # 在首次啟動時執行資料庫初始化
        init_db()

    # 註冊 Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    return app

# 開發伺服器入口
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
