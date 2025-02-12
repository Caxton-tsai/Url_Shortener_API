from flask import Flask, request, jsonify, redirect
from urllib.parse import urlparse
import hashlib
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

YOUR_API_URL = "http://127.0.0.1:3000/"

app = Flask(__name__)
url_map = {} #存短網址與原始網址的對應關係
limiter = Limiter(get_remote_address, app=app)

#驗證URL格式
def is_valid_url(url):
    try:
        result = urlparse(url)
        return (
            " " not in url and  #URL不能有空格
            result.scheme in {"http", "https"} and #網址必須http or https
            bool(result.netloc)  #必須有網域
        )
    except ValueError:
        return False

#產生短網址
def create_short_url(original_url):
    """用時間加原本網址做hash，降低碰撞"""
    current_time = datetime.datetime.utcnow().isoformat() #當前時間轉字串
    combined_string = original_url + current_time
    hash_object = hashlib.sha256(combined_string.encode())
    short_hash = hash_object.hexdigest()[:6]
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=30) #設定過期時間為30天後
    
    return f"{YOUR_API_URL}{short_hash}", expiration_date

#api 1：縮址
@app.route("/short_url", methods=["POST"])
@limiter.limit("1000 per minute") #速率限制，每個IP每分鐘最多n次
def create_short_url_api():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"success": False, "reason": f"Invalid JSON format: {str(e)}"}), 400

    #檢查request資料
    original_url = data.get("original_url", "").strip()
    if not original_url:
        return jsonify({"success": False, "reason": "Missing 'original_url'"}), 400

    #檢查URL資料型別
    if not isinstance(original_url, str):
        return jsonify({"success": False, "reason": "Invalid URL type"}), 400

    #檢查URL格式
    if not is_valid_url(original_url):
        return jsonify({"success": False, "reason": "Invalid URL"}), 400

    #檢查URL長度
    if len(original_url) > 2048:
        return jsonify({"success": False, "reason": "URL is too long"}), 414

    #產生短網址並儲存
    short_url, expiration_date = create_short_url(original_url)
    url_map[short_url] = {"original_url": original_url, "expiration_date": expiration_date}
    print(url_map)
    return jsonify({
        "short_url": short_url,
        "expiration_date": expiration_date.isoformat(),
        "success": True
    }), 201

#api 2：重新導向
@app.route("/<short_url>", methods=["GET"])
@limiter.limit("1000 per minute")  #速率限制，每個IP每分鐘最多n次
def redirect_to_original_api(short_url):
    short_url = f"{YOUR_API_URL}{short_url}"
    
    # 檢查短網址是否存在
    if short_url not in url_map:
        return jsonify({"success": False, "reason": "Short URL is not found"}), 404

    url_data = url_map[short_url]
    expiration_date_str = str(url_data["expiration_date"])
    expiration_date = datetime.datetime.fromisoformat(expiration_date_str)

    if datetime.datetime.utcnow() > expiration_date:
        return jsonify({"success": False, "reason": "Short URL has expired"}), 410

    return redirect(url_data["original_url"], code=302)

#速率限制的錯誤回應
@app.errorhandler(429)
def ratelimit_exceeded(e):
    return jsonify({"success": False, "reason": "Too many requests, please try again later."}), 429

if __name__ == "__main__":
    app.run(port=3000)
