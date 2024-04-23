from mmocr.apis import TextRecInferencer
import os
import json
import shutil


def count_correct_texts(folder_path, total_json_path):
    # 初始化正确文本计数器和总文件计数器
    word_acc_count = 0
    word_acc_ignore_case_count = 0
    total_count = 0

    text_map = {}
    with open(total_json_path, 'r') as file:
        data = json.load(file)
        for item in data['data_list']:
            for instance in item['instances']:
                img_path = item['img_path']
                text = instance['text']
                text_map[img_path] = text

    # 遍历文件夹中的所有文件
    if not os.path.exists(os.path.join(os.path.dirname(folder_path), 'word_acc')):
        os.makedirs(os.path.join(os.path.dirname(folder_path), 'word_acc'))
    if not os.path.exists(os.path.join(os.path.dirname(folder_path), 'word_acc_ignore_case')):
        os.makedirs(os.path.join(os.path.dirname(folder_path), 'word_acc_ignore_case'))
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 检查文件是否为JSON文件
        if filename.endswith('.json'):
            total_count += 1

            # 读取JSON文件内容
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    text = data['text']
                    # 获取文件名（去掉后缀）
                    file_name_without_extension = os.path.splitext(filename)[0]

                    filename_jpg = file_name_without_extension + '.jpg'
                    if filename_jpg in text_map:
                        # 完全准确
                        if text == text_map[filename_jpg]:
                            word_acc_count += 1
                        else:
                            shutil.copy(os.path.join(os.path.dirname(folder_path), 'vis', file_name_without_extension) + '.jpg',
                                        os.path.join(os.path.dirname(folder_path), 'word_acc', file_name_without_extension) + '.jpg')
                        # 忽略大小写
                        if text.lower() == text_map[filename_jpg].lower():
                            word_acc_ignore_case_count += 1
                        else:
                            shutil.copy(os.path.join(os.path.dirname(folder_path), 'vis', file_name_without_extension) + '.jpg',
                                        os.path.join(os.path.dirname(folder_path), 'word_acc_ignore_case', file_name_without_extension) + '.jpg')
                    else:
                        print("filename_jpg无法匹配：" + filename_jpg)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file {filename}: {e}")

    return word_acc_count, word_acc_ignore_case_count, total_count


def find_innermost_folders(folder_path):
    innermost_folders = []

    # 递归函数，用于在给定的文件夹路径下查找最里面的文件夹
    def find_innermost_helper(current_path):
        subfolders = [f for f in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, f))]
        if not subfolders:
            # 如果当前路径下没有子文件夹，说明当前路径是最里面的文件夹
            innermost_folders.append(current_path)
        else:
            # 递归地在每个子文件夹中查找最里面的文件夹
            for subfolder in subfolders:
                find_innermost_helper(os.path.join(current_path, subfolder))

    find_innermost_helper(folder_path)
    return innermost_folders


model_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster/TAL_ocren_IAM__90/TAL_ocren_IAM.py'
weight_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster/TAL_ocren_IAM__90/epoch_90.pth'
# 读取模型
inferencer = TextRecInferencer(model=model_path, weights=weight_path, device='cuda:0')

input_path = 'm_testout/m_img'
output_path = 'm_testout/TAL_ocren_IAM'
json_path = os.path.join(output_path, 'preds')
total_json_path = 'm_testout/newtest.json'

if not os.path.exists(output_path):
    os.makedirs(output_path)
innermost_folders = find_innermost_folders(input_path)
if innermost_folders:
    for folder in innermost_folders:
        # 推理
        inferencer(folder, out_dir=output_path, save_pred=True, save_vis=True)
        word_acc_count, word_acc_ignore_case_count, total_count = count_correct_texts(json_path, total_json_path)
        with open(os.path.join(output_path, 'path.txt'), 'w') as file:
            file.write('model_path:\n' + model_path)
            file.write('\nweight_path:\n' + weight_path)
            file.write(f'\n完全准确率: {word_acc_count}/{total_count}')
            file.write(f'\n忽略大小写准确率: {word_acc_ignore_case_count}/{total_count}')
        print(f"完全准确率: {word_acc_count}/{total_count}")
        print(f"忽略大小写准确率: {word_acc_ignore_case_count}/{total_count}")
else:
    print("该文件夹为空或只包含子文件夹。")
