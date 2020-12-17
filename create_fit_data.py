import json
import os

from src.twitter_tl import init_twitter_api, get_img_data_from_TL, download_file
from src.fit_image_ocr import file_ocr
from src.graph import create_graph

USER_ID = "tumugi3205"
SERCH_TEXT = "リングフィットアドベンチャー"
END_MONTH = 3

IMPORT_FILE_PATH = "output/ocr_result.json"
OUTPUT_FILE_PATH = "output/graph.png"
if __name__ == "__main__":
    with open("config/config.json") as f:
        CONFIG = json.load(f)

    # twitter APIの設定
    api = init_twitter_api(CONFIG)

    # 特定ユーザーのTLから特定文言の入ったツイートを取得、そこに入ってる画像の一枚目のURLを取得
    image_url_list = get_img_data_from_TL(api, USER_ID, SERCH_TEXT, END_MONTH)

    # 取得した画像URLからDL(ファイル名はツイート日時)
    for data in image_url_list:
        try:
            os.mkdir("get_data")
        except:
            pass
        dst_path = f"get_data/{data['created_at'].strftime('%Y-%m-%d')}.png"
        download_file(data['img_url'],dst_path)
    
    # DLした画像ファイルからデータ作成、出力
    ocr_data = file_ocr("./get_data")
    try:
        os.makedirs(IMPORT_FILE_PATH.replace(IMPORT_FILE_PATH.split("/")[-1], ""))
    except:
        pass
    with open(IMPORT_FILE_PATH, "w") as f:
        json.dump(ocr_data, f, indent=2)
    
    create_graph(IMPORT_FILE_PATH, OUTPUT_FILE_PATH)
