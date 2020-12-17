# import boto3

# # Amazon Textract client
# textract = boto3.client('textract', region_name="ap-southeast-1")

# # read image to bytes
# with open('get_data/2020-09-28.png', 'rb') as f:
#     data = f.read()

# # Call Amazon Textract
# response = textract.detect_document_text(
#     Document={
#         'Bytes': data
#     }
# )

# # Print detected text
# for item in response["Blocks"]:
#     if item["BlockType"] == "LINE":
#         print ('\033[94m' +  item["Text"] + '\033[0m')

import json


# 文字と右下座標のみのデータに整形
def get_word(data: dict) -> dict:
    words = []
    for item in data["Blocks"]:
        if item["BlockType"] == "WORD":
            words.append({
                "word":item["Text"],
                "right_bottom":item["Geometry"]["Polygon"][2]
            })
    return words

# 右下座標が特定付近(ずれ0.01まで許容)かの判定
def point_check(x: float, y: float) -> dict:
    origin_point = {
        "time":{"x":0.71,"y":0.46},
        "kcal":{"x":0.73,"y":0.63},
        "km":{"x":0.73,"y":0.78}
    }
    for k, v in origin_point.items():
        if abs(x-v["x"])<0.01 and abs(y-v["y"])<0.01:
            return k
     
# データの編集、格納までおこなう
def get_point_data(data: dict) -> dict:
    prepro_data = get_word(data)
    some_data = {}
    for v in prepro_data:
        tmp = point_check(v["right_bottom"]["X"], v["right_bottom"]["Y"])
        if tmp:
            some_data[tmp] = v["word"]
    return some_data


if __name__ == '__main__':
    with open("j.json") as f:
        data = json.load(f)
    d = get_point_data(data)
    print(d)
