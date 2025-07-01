from flask import jsonify


# 响应结果
# 通用响应格式化函数
def response(success, msg, data=None):
    return jsonify({"code": 0 if success else -1,
                    "message": msg,
                    "data": data})

# 注册全局异常处理，使所有 HTTPException 返回统一的 JSON 结构

def register_error_handlers(app):
    """Attach a handler that converts Werkzeug HTTPExceptions to JSON responses.

    Usage:
        from utils import register_error_handlers
        register_error_handlers(app)
    """
    from werkzeug.exceptions import HTTPException  # type: ignore

    @app.errorhandler(HTTPException)  # type: ignore[misc]
    def handle_http_exception(exc: HTTPException):  # noqa: WPS430
        response = jsonify({
            "code": -1,
            "message": exc.description,
            "data": None,
        })
        response.status_code = exc.code  # Preserve original status code (e.g., 400, 404)
        return response
