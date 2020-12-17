from typing import Any
from PIL import Image
import pyocr
import cv2
import sys
import re
import os
import json


def startup_ocr() -> Any:
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    return tools[0]

def get_file_name(file_path: str) -> str:
    return file_path.split("/")[-1].split(".")[0]

def overview_preprosess(file_path: str) -> dict:
    file_name = get_file_name(file_path)
    img = Image.open(file_path)
    width_section = img.width/4
    height_section = img.height/6
    create_path = {}

    rect_dic = {
        "time": (600, 250, 770, 320),
        "kcal": (width_section*2, height_section*3, width_section*3,height_section*4),
        "km": (width_section*2, height_section*4, width_section*3,height_section*5)
    }

    for name, rect in rect_dic.items():
        try:
            os.mkdir("prepro")
        except:
            pass
        output_path = f"prepro/{file_name}_{name}.jpg"
        prepro = img.crop(box=(rect))
        prepro.save(output_path, format="jpeg")
        create_path[name] = output_path

    return create_path

def post_processing(ocr_text_dict: dict) -> dict:
    for name, text in ocr_text_dict.items():                
        ocr_text_dict[name] = ocr_text_dict[name].replace("A", "4").replace("．", ".").replace("Zu", "2.").replace("o", "0").replace(" ", "").replace("]", "1")
        ocr_text_dict[name] = re.sub("[a-zA-Z]","", ocr_text_dict[name])
        
        if name == "time":
            if len(ocr_text_dict[name])>2:
                ocr_text_dict[name] = ocr_text_dict[name][:2]
        if  len(ocr_text_dict[name])>4 and "." not in ocr_text_dict[name]:
            ocr_text_dict[name] = f"{ocr_text_dict[name][:len(ocr_text_dict[name])-2]}.{ocr_text_dict[name][-2:]}"

        try:
            ocr_text_dict[name] = float(ocr_text_dict[name])
            if ocr_text_dict[name] > 200:
                raise Exception
        except:
            if name != "read_file_name":
                ocr_text_dict[name] = "error"
    return ocr_text_dict
        
def file_ocr(do_dir: list) -> list:
    ocr_list = []
    tool = startup_ocr()    
    for filename in os.listdir(do_dir):
        ocr_text_dict = {}
        output_path = overview_preprosess(f"{do_dir}/{filename}")
        for name, path in output_path.items():
            img = cv2.imread(path)
            lang = "eng"
            ocr_text_dict[name] = tool.image_to_string(Image.open(path), lang=lang)

        ocr_text_dict = post_processing(ocr_text_dict)
        ocr_text_dict["read_file_name"] = filename
        ocr_list.append(ocr_text_dict)
    return ocr_list

if __name__ == "__main__":
    ocr_data = file_ocr("./get_data")
    with open("output/ocr_result.json", "w") as f:
        json.dump(ocr_data, f, indent=2)
