from flask import Flask, request, jsonify, redirect
from urllib.parse import urlparse
import hashlib
from datetime import datetime, timedelta


import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler



load_dotenv()
MONGO_CLIENT = os.getenv("MONGO_CLIENT")
client = MongoClient(MONGO_CLIENT)
database = client.senaonetworks #選db
YOUR_API_URL = "http://127.0.0.1:3000/"
REQUEST_RATE_LIMIT = "1000 per minute"

app = Flask(__name__)
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
    current_time = datetime.utcnow().isoformat() #當前時間轉字串
    combined_string = original_url + current_time
    hash_object = hashlib.sha256(combined_string.encode())
    short_hash = hash_object.hexdigest()[:6]
    db_location = "/" + (str(datetime.today().date())[2:]).replace("-", "")
    expiration_date = datetime.utcnow() + timedelta(days=30) #設定過期時間為30天後

    return f"{YOUR_API_URL}{short_hash}{db_location}", expiration_date

#api 1：縮址
@app.route("/short_url", methods=["POST"])
@limiter.limit(REQUEST_RATE_LIMIT) #速率限制，每個IP每分鐘最多n次
def create_short_url_api():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"success": False, "reason": f"Invalid JSON format: {str(e)}"}), 415

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
    current_date = str(datetime.today().date())
    database[current_date].insert_one({
            "short_url" : short_url,
            "original_url" : original_url,
            "expiration_date" : expiration_date
        })
    
    return jsonify({
        "short_url": short_url,
        "expiration_date": expiration_date.isoformat(),
        "success": True
    }), 201

#api 2：重新導向
@app.route("/<short_url>/<db_location>", methods=["GET"])
@limiter.limit(REQUEST_RATE_LIMIT)  #速率限制，每個IP每分鐘最多n次
def redirect_to_original_api(short_url,db_location):
    short_url = f"{YOUR_API_URL}{short_url}/{db_location}"
    db_location = "20" + db_location[:2] + "-" + db_location[2:4] + "-" + db_location[4:]
    
    #檢查短網址是否存在
    if db_location not in database.list_collection_names():
        return jsonify({"success": False, "reason": "Short URL is not found"}), 404
    
    url_data = database[db_location].find_one({"short_url" : short_url})
    if not url_data:
        return jsonify({"success": False, "reason": "Short URL is not found"}), 404

    expiration_date_str = str(url_data["expiration_date"])
    expiration_date = datetime.fromisoformat(expiration_date_str)

    #檢查是否過期
    if datetime.utcnow() > expiration_date:
        return jsonify({"success": False, "reason": "Short URL has expired"}), 410

    return redirect(url_data["original_url"], code=302)

#速率限制的錯誤回應
@app.errorhandler(429)
def ratelimit_exceeded(e):
    return jsonify({"success": False, "reason": "Too many requests, please try again later."}), 429

#刪除過期short_url
def delete_expired_short_urls():
    today = datetime.today()
    thirty_one_days_ago_date = str((today - timedelta(days=31)).date())
    if thirty_one_days_ago_date in database.list_collection_names():
        database.drop_collection(thirty_one_days_ago_date)
        print(f"集合 {thirty_one_days_ago_date} 已刪除。")
    else:
        print(f"集合 {thirty_one_days_ago_date} 不存在，無需刪除。")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_short_urls, "cron", hour=0, minute=0) #每天凌晨00:00執行
    scheduler.start()
    print("排程已啟動，每天00:00刪除過期短網址。")
    

if __name__ == "__main__":
    scheduler = start_scheduler()
    app.run("0.0.0.0",port=3000)
