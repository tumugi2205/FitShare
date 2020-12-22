import json
import os

from src.textract import do_ocr, get_point_data, post_processing
from src.graph import create_graph

IMPORT_FILE_PATH = "output/ocr_result.json"
OUTPUT_FILE_PATH = "output/graph2.png"
if __name__ == "__main__":
    with open("./output/res.json") as f:
        data = json.load(f)
    # data = do_ocr("./get_data")
    word_point_list = []
    for word_dict in data:
        word_point_list.append(get_point_data(word_dict))
    word_point_list = post_processing(word_point_list)
    with open("./output/j.json", "w") as f:
        json.dump(word_point_list, f)
    
    # DLした画像ファイルからデータ作成、出力
    try:
        os.makedirs(IMPORT_FILE_PATH.replace(IMPORT_FILE_PATH.split("/")[-1], ""))
    except:
        pass
    with open(IMPORT_FILE_PATH, "w") as f:
        json.dump(word_point_list, f, indent=2)
    
    create_graph(IMPORT_FILE_PATH, OUTPUT_FILE_PATH)
