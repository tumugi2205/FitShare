import json
import urllib
from datetime import datetime

import tweepy
from dateutil.relativedelta import relativedelta


# tweepyの初期化
def init_twitter_api(config: dict) -> object:
    auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
    auth.set_access_token(config['ACCESS_TOKEN'], config['ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)

# twitterから、end_date日前までのデータ取得
def get_img_data_from_TL(api: object, user_id: str, serch_text: str, end_date: int) -> object:
    image_url_list = []
    print(f"get {user_id}'s TL now...")
    search_results = tweepy.Cursor(api.user_timeline, screen_name=user_id).items()
    today = datetime.today()
    lastmonth = today - relativedelta(months=end_date)
    print(f"get [{serch_text}] until {lastmonth}")
    for i, result in enumerate(search_results):
        try:
            if i%50 == 0:
                print('.')
            if result.created_at < lastmonth:
                break
            if serch_text in result.text:
                image_url_list.append(
                    {
                        "created_at": result.created_at,
                        "img_url": result.extended_entities["media"][0]["media_url"]
                    }
                )
        except Exception as e:
            print(e)
    return image_url_list

# 画像のDL
def download_file(url: str, dst_path: str) -> None:
   try:
       with urllib.request.urlopen(url) as web_file:
           data = web_file.read()
           with open(dst_path, mode="wb") as local_file:
               local_file.write(data)
   except urllib.error.URLError as e:
       print(e)


if __name__ == "__main__":
    user_id = "tumugi3205"
    serch_text = "リングフィットアドベンチャー"
    end_date = 3
    with open("config/config.json") as f:
        conf = json.load(f)
    api = init_twitter_api(conf)
    image_url_list = get_img_data_from_TL(api, user_id, serch_text, end_date)
    for data in image_url_list:
        dst_path = f"get_data/{data['created_at'].strftime('%Y-%m-%d')}.png"
        download_file(data['img_url'],dst_path)

