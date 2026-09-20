import json
def load_data():
    with open("school_info.json", "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(school_info):
    with open("school_info.json", "w", encoding="utf-8") as file:
        json.dump(school_info, file, ensure_ascii=False, indent=4)