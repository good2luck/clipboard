from flask import jsonify


# 响应结果
# 通用响应格式化函数
def response(success, msg, data=None):
    return jsonify({"code": 0 if success else -1,
                    "message": msg,
                    "data": data})
