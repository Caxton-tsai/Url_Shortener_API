# Url_Shortener_API

這是一個簡單的縮網址 API，允許用戶將長網址轉換為短網址，並能夠在有效期內進行重定向。此API使用Flask框架開發，並採用限流來避免濫用。

## API 功能
### 1. 縮網址 (POST YOUR_API_URL/short_url)

將一個長網址提交給 API，並返回對應的短網址，依照自己的伺服器網址輸入YOUR_API_URL。  
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
- 400: 請求的格式或資料結構錯誤，或缺少必要的參數，或URL的格式錯誤。
- 414: 請求的 URL 過長，超過最大長度 2048 字符。
- 415: 請求帶入的body非json格式。


### 2. 重新導向 (GET YOUR_API_URL/"Returned_short_URL")
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

### 3. 速率限制
為了防止濫用，可以自訂速率限制。可以修改REQUEST_RATE_LIMIT變數。  
變數範例： REQUEST_RATE_LIMIT = "10 per minute"

### 4. 錯誤處理
此 API 會返回不同的錯誤碼來處理常見的問題：

- 400 Bad Request: 請求的格式或資料結構錯誤，或缺少必要的參數，或URL的格式錯誤。
- 404 Not Found: 短網址未在資料庫找到。
- 410 Gone: 短網址已過期。
- 414 URI Too Long: 請求的URL過長，超過最大長度2048字符。
- 415 Unsupported Media Type: 請求的資料格式不受支持。
- 429 Too Many Requests: 請求頻率過高，請稍後再試。

如何使用
1. 發送 POST 請求到 /short_url，並在請求主體中包含原始網址 (original_url)。
2. 根據回應中的短網址 (short_url) 進行後續操作。
3. 發送 GET 請求到 /:short_url，以短網址作為 URL 路徑，將會被重定向到對應的原始網址。
