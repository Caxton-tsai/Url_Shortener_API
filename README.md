# Url_Shortener_API

這是一個簡單的縮網址 API，允許用戶將長網址轉換為短網址，並能夠在有效期內進行重定向。此API使用Flask框架開發，並採用限流來避免濫用。

## API 功能
### 1. 縮網址 (POST YOUR_API_URL/short_url)

將一個長網址提交給 API，並返回對應的短網址，依照自己的伺服器網址修改程式碼 YOUR_API_URL變數。  
變數範例： YOUR_API_URL = "http://127.0.0.1:3000/"

請求範例：  
URL: http://127.0.0.1:3000/short_url  
方法: POST

request body (JSON)：
{
  "original_url": "https://www.example.com"
}

回應範例：  
回應成功 (HTTP 201):  
{
  "success": true,
  "short_url": "http://127.0.0.1:3000/abc123",
  "expiration_date": "2025-03-14T12:34:56"
}

回應錯誤 (HTTP 400):  
{
  "success": false,
  "reason": "Invalid URL"
}

參數說明：
- original_url: 必須是有效的URL格式。

代碼說明：
- 201 Created: 請求已成功，產生short url。
- 400 Bad Request: 請求的格式或資料結構錯誤，或缺少必要的參數，或URL的格式錯誤。
- 414 URI Too Long: 請求的 URL 過長，超過最大長度 2048 字符。
- 415 Unsupported Media Type: 請求帶入的body非json格式。
- 429 Too Many Requests: 請求頻率過高，請稍後再試。

### 2. 重新導向 (GET YOUR_API_URL/<得到的short_url>)
通過短網址重定向到原始網址。

請求範例：  
URL: http://127.0.0.1:3000/abc123  
方法: GET

回應範例：  
回應成功 (HTTP 302):  
用戶將被重定向到原始網址。

回應錯誤 (HTTP 404):
{
  "success": false,
  "reason": "Short URL is not found"
}

代碼說明：
- 302 Found: 請求已成功，並redirect。
- 404 Not Found: 短網址未在資料庫找到。
- 410 Gone: 短網址已過期。
- 429 Too Many Requests: 請求頻率過高，請稍後再試。

### 3. 速率限制
為了防止濫用，可以自訂速率限制。可以修改REQUEST_RATE_LIMIT變數。  
變數範例： REQUEST_RATE_LIMIT = "10 per minute"

### 4. 錯誤處理
統整錯誤碼

- 400 Bad Request: 請求的格式或資料結構錯誤，或缺少必要的參數，或URL的格式錯誤。
- 404 Not Found: 短網址未在資料庫找到。
- 410 Gone: 短網址已過期。
- 414 URI Too Long: 請求的URL過長，超過最大長度2048字符。
- 415 Unsupported Media Type: 請求的資料格式不受支持。
- 429 Too Many Requests: 請求頻率過高，請稍後再試。

### 5. 如何使用
1. 發送 POST 請求到 YOUR_API_URL/short_url，並在request body中以json格式送出，包含原始網址。
2. 根據response中的短網址<得到的short_url>進行後續操作。
3. 發送 GET 請求到 YOUR_API_URL/<得到的short_url>，以短網址作為URL路徑，將會被重定向到對應的原始網址。

## Docker 容器使用說明
這個 Docker 映像檔包含了 URL 短網址 API，並且會在 3000 端口上監聽請求。您可以透過瀏覽器或任何 HTTP 客戶端（例如 Postman）來訪問這個 API。

### 如何使用 Docker 容器
1. **拉取 Docker 映像檔**：您可以從 Docker Hub 拉取預先建置好的映像檔：
    ```bash
    docker pull caxtontsai/my-flask-api
    ```
    
2. **運行 Docker 容器**：拉取映像檔後，您可以在本地機器或伺服器上運行容器：
    ```bash
    docker run -p 3000:3000 caxtontsai/my-flask-api
    ```



