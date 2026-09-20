import json
import os

def make_data():
    if os.path.exists("school_info.json"):
        return

    school_info = {
        "school_classes": [],
        "teachers": [],
        "students": []
    }

    save_data(school_info)


def load_data():
    make_data()
    with open("school_info.json", "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(school_info):
    with open("school_info.json", "w", encoding="utf-8") as file:
        json.dump(school_info, file, ensure_ascii=False, indent=4)