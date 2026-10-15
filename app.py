"""
app.py - Web Server phục vụ Game "Thắm & Thơ Đi Học Về" trên nền tảng Cloud (Render.com)
"""

import os
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    """Phục vụ trang chủ chứa trò chơi HTML5."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/health')
def health():
    """Health check endpoint cho Render.com monitoring."""
    return jsonify({
        "status": "healthy",
        "game": "Thắm & Thơ Đi Học Về",
        "platform": "Render Cloud"
    })

@app.route('/<path:path>')
def serve_static(path):
    """Phục vụ các file assets, ảnh chân dung, âm thanh mp3."""
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Render.com tự động cung cấp biến môi trường PORT (mặc định 10000 hoặc 5000)
    port = int(os.environ.get('PORT', 5000))
    print(f"=====================================================")
    print(f"  GAME THẮM & THƠ ĐANG CHẠY TẠI: http://localhost:{port}")
    print(f"=====================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
