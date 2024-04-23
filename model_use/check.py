import os
import json


def check_folder_names(dirfolder, txt_file_path, folder_path, json_path):
    no_dir = []
    no_txt = []
    no_json_dir = []
    no_dir_json = set()
    # 获取指定文件夹中的所有一级子文件夹名称
    folder_names = next(os.walk(folder_path))[1]

    # # txt比dir多的
    # with open(txt_file_path, "r") as txt_file:
    #     lines = txt_file.readlines()

    # for line in lines:
    #     # 获取第一个空格前的元素
    #     first_element = line.strip().split()[0]
    #     second_element = line.strip().split()[1]

    #     # 检查是否与文件夹中的一级子文件夹名称对应
    #     if first_element not in folder_names:
    #         if second_element == 'unprocessed1' or second_element == 'unprocessed2' or second_element == 'unprocessed3' or second_element == 'unprocessed4':
    #             no_dir.append(first_element)

    # # txt比dir少的
    # with open(txt_file_path, "r") as txt_file:
    #     lines = txt_file.readlines()
    #     cleanline = []
    #     for line in lines:
    #         cleanline.append(line.strip().split()[0])
    # for folder in folder_names:
    #     if folder not in cleanline:
    #         no_txt.append(folder)

    # json比dir多的
    with open(json_path, "r") as file:
        data = json.load(file)
        for item in data["data_list"]:
            a = 0
            for folder in folder_names:
                if item["img_path"].split('/')[0] == folder:
                    a = 1
                    break
            if a == 0:
                no_json_dir.append(item["img_path"])

    # json比dir少的
    with open(json_path, "r") as file:
        data = json.load(file)
        for folder in folder_names:
            for item in data["data_list"]:
                a = 0
                if item["img_path"].split('/')[0] == folder:
                    a = 1
                    break
            if a == 0:
                no_dir_json.add(folder)

    # with open(os.path.join(dirfolder, 'nodir.txt'), "w") as m_txt1:
    #     for x in no_dir:
    #         m_txt1.write(x + '\n')

    # with open(os.path.join(dirfolder, 'notxt.txt'), "w") as m_txt2:
    #     for y in no_txt:
    #         m_txt2.write(y + '\n')

    with open(os.path.join(dirfolder, 'nojsondir.txt'), "w") as m_txt3:
        for y in no_json_dir:
            m_txt3.write(y + '\n')

    with open(os.path.join(dirfolder, 'nodirjson.txt'), "w") as m_txt4:
        for y in no_dir_json:
            m_txt4.write(y + '\n')


# 指定txt文件路径和文件夹路径
dirfolder = os.path.dirname(os.path.abspath(__file__))
txt_file_path = os.path.join(dirfolder, "condition.txt")
folder_path = 'data/TAL/origin'
json_path = 'data/TAL/train.json'

# 调用函数检查文件
check_folder_names(dirfolder, txt_file_path, folder_path, json_path)
