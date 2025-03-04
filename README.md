# Url_Shortener_API

This is a simple URL shortening API that allows users to convert long URLs into short URLs and redirect them within a valid period. The API is developed using the Flask framework and implements rate limiting to prevent abuse.

## API Features
### 1. Shorten URL (POST YOUR_API_URL/short_url)

Submit a long URL to the API and it will return the corresponding short URL. Modify the `YOUR_API_URL` variable to match your server URL.  
Example for the variable: `YOUR_API_URL = "http://127.0.0.1:3000/"`

Request Example:  
URL: http://127.0.0.1:3000/short_url  
Method: POST

Request body (JSON):
{
  "original_url": "https://www.example.com"
}

Response Example:  
Successful response (HTTP 201):
{
  "success": true,
  "short_url": "http://127.0.0.1:3000/abc123",
  "expiration_date": "2025-03-14T12:34:56"
}

Error response (HTTP 400):
{
  "success": false,
  "reason": "Invalid URL"
}

Parameter Explanation:
- `original_url`: Must be a valid URL format.

Status Code Explanation:
- 201 Created: The request was successful, and the short URL was generated.
- 400 Bad Request: The request format or data structure is incorrect, or a required parameter is missing, or the URL format is invalid.
- 414 URI Too Long: The requested URL is too long and exceeds the maximum length of 2048 characters.
- 415 Unsupported Media Type: The body of the request is not in JSON format.
- 429 Too Many Requests: The request frequency is too high; please try again later.

### 2. Redirect (GET YOUR_API_URL/<obtained_short_url>)

Redirect from the short URL to the original URL.

Request Example:  
URL: http://127.0.0.1:3000/abc123  
Method: GET

Response Example:  
Successful response (HTTP 302):  
The user will be redirected to the original URL.

Error response (HTTP 404):
{
  "success": false,
  "reason": "Short URL is not found"
}

Status Code Explanation:
- 302 Found: The request was successful, and a redirect occurred.
- 404 Not Found: The short URL was not found in the database.
- 410 Gone: The short URL has expired.
- 429 Too Many Requests: The request frequency is too high; please try again later.

### 3. Rate Limiting
To prevent abuse, rate limits can be customized by modifying the `REQUEST_RATE_LIMIT` variable.  
Example variable: `REQUEST_RATE_LIMIT = "10 per minute"`

### 4. Error Handling
Consolidated error codes:

- 400 Bad Request: The request format or data structure is incorrect, or a required parameter is missing, or the URL format is invalid.
- 404 Not Found: The short URL was not found in the database.
- 410 Gone: The short URL has expired.
- 414 URI Too Long: The requested URL is too long and exceeds the maximum length of 2048 characters.
- 415 Unsupported Media Type: The request data format is not supported.
- 429 Too Many Requests: The request frequency is too high; please try again later.

### 5. How to Use
1. Send a POST request to `YOUR_API_URL/short_url` with the original URL in the request body as JSON format.
2. Use the short URL from the response `<obtained_short_url>` for subsequent actions.
3. Send a GET request to `YOUR_API_URL/<obtained_short_url>`, where the short URL will redirect you to the original URL.

## Docker Container Usage
This Docker image contains the URL shortening API and listens on port 3000 for requests. You can access the API via a browser or any HTTP client (e.g., Postman).

### How to Use the Docker Container
1. **Pull the Docker image**: You can pull the pre-built image from Docker Hub:
    ```bash
    docker pull caxtontsai/my-flask-api
    ```

2. **Run the Docker container**: After pulling the image, you can run the container on your local machine or server:
    ```bash
    docker run -p 3000:3000 caxtontsai/my-flask-api
    ```


 
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



