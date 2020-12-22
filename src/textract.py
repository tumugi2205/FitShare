import json
import os
import re

import boto3

# Amazon Textract client
textract = boto3.client('textract', region_name="ap-southeast-1")

def do_ocr(do_dir: str) -> list:
    res_list = []
    file_list = []
    for filename in os.listdir(do_dir):
        # read image to bytes
        with open(f"{do_dir}/{filename}", 'rb') as f:
            data = f.read()

        # Call Amazon Textract
        res = textract.detect_document_text(
                Document={
                    'Bytes': data
                }
            )
        res["date"] = filename
        res_list.append(res)
    with open("./output/res.json", "w") as f:
        json.dump(res_list, f)
    return res_list



# 文字と右下座標のみのデータに整形
def get_word(data: dict) -> dict:
    words = []
    for item in data["Blocks"]:
        if item["BlockType"] == "WORD":
            words.append({
                "word":item["Text"],
                "right_bottom":item["Geometry"]["Polygon"][2],
            })
    words.append({"date": data["date"]})
    return words

# 右下座標が特定付近(ずれ0.01まで許容)かの判定
def point_check(x: float, y: float) -> dict:
    origin_point = {
        "time":{"x":0.71,"y":0.46},
        "kcal":{"x":0.73,"y":0.63},
        "km":{"x":0.73,"y":0.78}
    }
    for k, v in origin_point.items():
        if abs(x-v["x"])<0.03 and abs(y-v["y"])<0.03:
            return k
     
# データの編集、格納までおこなう
def get_point_data(data: dict) -> dict:
    prepro_data = get_word(data)
    some_data = {}
    for v in prepro_data:
        if "date" in v:
            some_data["read_file_name"] = v["date"]
        else:
            tmp = point_check(v["right_bottom"]["X"], v["right_bottom"]["Y"])
            if tmp and any(chr.isdigit() for chr in v["word"]):
                some_data[tmp] = v["word"]
    return some_data

def post_processing(word_point_list: list):
    for data in word_point_list:
        if "time" not in data:
            data["time"] = "0"
        re_data = re.sub('[^0-9]','', data["time"])
        if len(re_data) < 2:
            re_data = re_data[:1]
        else:
            re_data = re_data[:2]
        data["time"] = float(re_data) if float(re_data) < 40 else float(re_data)/10
        data["kcal"] = float(data["kcal"].replace("o","0").replace("O","0").replace("k","").replace("c","").replace("a","").replace("l",""))
        data["km"] = float(data["km"].replace("o","0").replace("O","0").replace("k","").replace("m",""))
    return word_point_list





if __name__ == '__main__':
    with open("./output/res.json") as f:
        data = json.load(f)
    # data = do_ocr("./get_data")
    word_point_list = []
    for word_dict in data:
        word_point_list.append(get_point_data(word_dict))
    word_point_list = post_processing(word_point_list)
    with open("./output/j.json", "w") as f:
        json.dump(word_point_list, f)
