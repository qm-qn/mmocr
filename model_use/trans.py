import json


def convert_text_to_lowercase(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 遍历data_list中的每一个字典，将text转换为小写
    for item in data['data_list']:
        for instance in item['instances']:
            instance['text'] = instance['text'].lower()

    # 将修改后的数据写回原始的JSON文件
    with open('data/ocren2100/test.json', 'w') as f:
        json.dump(data, f, indent=4)


# 调用函数，传入JSON文件路径
convert_text_to_lowercase("data/ocren2100/train.json")
