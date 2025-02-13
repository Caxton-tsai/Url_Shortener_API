# 使用 Python 3.11 的官方映像
FROM python:3.11-slim

# 設定環境變數，減少不必要的提示
ENV PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 開放 Flask 的 3000 埠
EXPOSE 3000

# 設定容器啟動時執行的指令
CMD ["python", "main.py"]
