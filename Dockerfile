# 使用官方的 Python 3.10 slim 版本作为基础环境
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制整个项目结构到容器的 /app 目录下
COPY . .

# 设置环境变量，告诉 Python 模块的搜索路径
# 这是解决模块导入问题的关键
ENV PYTHONPATH=/app

# 安装所有 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 容器启动时要执行的命令
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

