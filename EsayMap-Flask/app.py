from flask import Flask
from flask_cors import CORS
from routes.infer import infer_bp
from routes.gp import gp_bp

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问

# 注册蓝图
app.register_blueprint(infer_bp, url_prefix='/api/infer')
app.register_blueprint(gp_bp, url_prefix='/api/gp')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
