import json
import time
import os
from flask import Flask, request, abort
import redis
from utils import response, register_error_handlers

app = Flask(__name__)

# 注册统一的 JSON 错误处理
register_error_handlers(app)

# 连接 Redis（通过环境变量配置，提升安全性与可移植性）
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD", ""),
    db=int(os.getenv("REDIS_DB", "0")),
    decode_responses=True,  # 自动解码 bytes -> str
)

# 设置缓存的时间（15min）
DEFAULT_EXPIRE_TIME = 15 * 60

# 保存
@app.route('/api/v1/clipboard/save', methods=['POST'])
def save_clipboard():
    data = request.json or {}
    password = data.get('password')
    content = data.get('content')

    # 参数校验
    if not password or not content:
        abort(400, description="Password and content are required")

    # 设置redis
    clipboard_data = {
        'content': content,
        'timestamp': time.time()
    }
    redis_key = f'clipboard:{password}'
    redis_client.rpush(redis_key, json.dumps(clipboard_data))
    redis_client.expire(redis_key, DEFAULT_EXPIRE_TIME)
    return response(True, '保存成功')


# 获取全部
@app.route('/api/v1/clipboard/list', methods=['POST'])
def list_clipboard():
    data = request.json or {}
    password = data.get('password')

    # 参数校验
    if not password:
        abort(400, description="Password is required")

    # 从redis中获取
    redis_list = redis_client.lrange(f'clipboard:{password}', 0, -1)

    # 若无数据则返回空数组
    if not redis_list:
        return response(True, '查询成功', {'clipboard_contents': []})

    clipboard_contents = []
    current_time = time.time()
    # 获取每个key
    for item_str in redis_list:
        item = json.loads(item_str)
        if item and (current_time - float(item['timestamp'])) < DEFAULT_EXPIRE_TIME:
            clipboard_contents.append({
                'content': item['content'],
                'timestamp': float(item['timestamp'])
            })
    return response(True, '查询成功', {'clipboard_contents': clipboard_contents})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
