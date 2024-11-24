import json
import time
from flask import Flask, request
import redis
from utils import response

app = Flask(__name__)

# 连接redis
redis_client = redis.StrictRedis(host='localhost', port=6379, password='admin', db=0)

# 设置缓存的时间（15min）
DEFAULT_EXPIRE_TIME = 15 * 60

# 保存
@app.route('/api/v1/clipboard/save', methods=['POST'])
def save_clipboard():
    data = request.json
    password = data.get('password')
    content = data.get('content')

    if not password or not content:
        return response(False, 'Password and content are required')

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
    password = request.json.get('password')

    if not password:
        return response(True, '查询成功', {'clipboard_contents': []})

    # 从redis中获取
    redis_list = redis_client.lrange(f'clipboard:{password}', 0, -1)
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
