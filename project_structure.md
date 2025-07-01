# 项目结构介绍

## 项目概述

这是一个基于Flask的剪贴板共享应用的后端服务，支持通过密码保护的方式在设备间共享剪贴板内容。

对应前端项目地址：https://github.com/good2luck/clipboard-app

项目部署细节，见博客文章：https://xudj.top/archives/clipboard

## 技术栈

- **后端框架**: Flask (Python)
- **数据库**: Redis (用于缓存和数据存储)
- **语言**: Python

## 项目结构

```
.
├── .git/                   # Git版本控制目录
├── .idea/                  # IDE配置目录(PyCharm/IntelliJ)
├── README.md               # 项目说明文档
├── app.py                  # 主应用文件，包含Flask应用和API路由
├── utils.py                # 工具函数模块
├── requirements.txt        # Python依赖包列表
├── img.png                 # 项目相关图片资源
└── img_1.png               # 项目相关图片资源
```

## 主要文件说明

### app.py
主应用文件，包含：
- Flask应用实例创建
- Redis连接配置
- API路由定义：
  - `POST /api/v1/clipboard/save` - 保存剪贴板内容
  - `POST /api/v1/clipboard/list` - 获取剪贴板历史记录
- 缓存过期时间设置（15分钟）

### utils.py
工具函数模块，包含：
- `response()` - 统一的API响应格式化函数

### requirements.txt
项目依赖：
- `flask` - Web框架
- `redis` - Redis客户端库

## 功能特性

1. **密码保护**: 使用密码作为唯一标识符来区分不同用户的剪贴板内容
2. **自动过期**: 剪贴板内容在15分钟后自动过期删除
3. **历史记录**: 支持查看同一密码下的所有剪贴板历史记录
4. **时间戳**: 每条记录都包含创建时间戳
5. **RESTful API**: 提供标准的HTTP API接口

## Redis数据结构

- **Key格式**: `clipboard:{password}`
- **数据类型**: List (列表)
- **数据内容**: JSON字符串，包含：
  ```json
  {
    "content": "剪贴板内容",
    "timestamp": 时间戳
  }
  ```

## API接口

### 保存剪贴板内容
- **URL**: `POST /api/v1/clipboard/save`
- **参数**: 
  ```json
  {
    "password": "密码",
    "content": "剪贴板内容"
  }
  ```

### 获取剪贴板列表
- **URL**: `POST /api/v1/clipboard/list`
- **参数**:
  ```json
  {
    "password": "密码"
  }
  ```

## 运行配置

- **端口**: 5001
- **调试模式**: 开启
- **Redis配置**: 
  - 主机: localhost
  - 端口: 6379
  - 密码: admin
  - 数据库: 0

这个项目结构简洁明了，专注于核心功能实现，适合作为轻量级的剪贴板共享服务。