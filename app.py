"""
app.py - Web Server phục vụ Game "Thắm & Thơ Đi Học Về" trên nền tảng Cloud (Render.com)
"""

import os
from flask import Flask, send_from_directory, jsonify, redirect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = BASE_DIR

app = Flask(__name__, static_folder=STATIC_DIR)

@app.route('/')
@app.route('/index.html')
@app.route('/game')
def index():
    """Phục vụ trang chủ chứa trò chơi HTML5."""
    for folder in [STATIC_DIR, BASE_DIR]:
        if os.path.exists(os.path.join(folder, 'index.html')):
            return send_from_directory(folder, 'index.html')
    return "Không tìm thấy file index.html!", 404

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
    # 1. Thử tìm trong STATIC_DIR
    if os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    # 2. Thử tìm trong BASE_DIR
    if os.path.exists(os.path.join(BASE_DIR, path)):
        return send_from_directory(BASE_DIR, path)
    # 3. Nếu path bắt đầu bằng static/
    if path.startswith('static/'):
        clean = path[len('static/'):]
        if os.path.exists(os.path.join(STATIC_DIR, clean)):
            return send_from_directory(STATIC_DIR, clean)
        if os.path.exists(os.path.join(BASE_DIR, clean)):
            return send_from_directory(BASE_DIR, clean)
    # 4. Fallback về index.html thay vì báo lỗi 404
    for folder in [STATIC_DIR, BASE_DIR]:
        if os.path.exists(os.path.join(folder, 'index.html')):
            return send_from_directory(folder, 'index.html')
    return "Not Found", 404

@app.errorhandler(404)
def not_found(e):
    """Tự động chuyển về index.html khi gặp lỗi 404."""
    for folder in [STATIC_DIR, BASE_DIR]:
        if os.path.exists(os.path.join(folder, 'index.html')):
            return send_from_directory(folder, 'index.html')
    return "Not Found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"=====================================================")
    print(f"  GAME THẮM & THƠ ĐANG CHẠY TẠI: http://localhost:{port}")
    print(f"=====================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
