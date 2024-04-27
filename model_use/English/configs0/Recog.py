from mmocr.apis import TextRecInferencer
import os
import json
from pathlib import Path
import shutil


def get_corresponding_path(original_path, original_folder_name, target_folder_name):
    path_parts = Path(original_path).parts
    modified_parts = [target_folder_name if part == original_folder_name else part for part in path_parts]
    return Path(*modified_parts)


def read_json_files(folder_path, json_path):
    with open(json_path, 'r') as file:
        data_list = json.load(file)
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                text = data['text']
                scores = data['scores']
                new_data = {
                    "img_path": os.path.splitext(filename)[0],
                    "text": text,
                    "scores": scores
                }
                data_list.append(new_data)
    result_json_path = os.path.dirname(folder_path) + ".json"
    with open(result_json_path, 'w') as file:
        json.dump(data_list, file)
    shutil.rmtree(os.path.dirname(folder_path))


def process_images_in_folder(folderIn_path, folder_save_folder, inferencer):
    if not os.path.exists(folder_save_folder):
        os.makedirs(folder_save_folder)
    rec_list = []
    for filename in os.listdir(folderIn_path):
        fileInpath = os.path.join(folderIn_path, filename)
        file_save_folder = os.path.join(folder_save_folder, filename)
        if os.path.isdir(fileInpath):
            process_images_in_folder(fileInpath, file_save_folder, inferencer)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            rec_list.append(fileInpath)
    if rec_list:
        inferencer(rec_list, out_dir=folder_save_folder, save_pred=True)
        read_json_files(os.path.join(folder_save_folder, 'preds'), get_corresponding_path(os.path.join(folderIn_path, "text.json"), "result", "delete_blank"))


def recog():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.dirname(current_dir)
    model_path = os.path.join(parent_dir, "model/config.py")
    weight_path = os.path.join(parent_dir, "model/weight.pth")
    inferencer = TextRecInferencer(model=model_path, weights=weight_path, device='cuda:0')
    folderIn_path = os.path.join(parent_dir, 'delete_blank')
    folder_save_folder = os.path.join(parent_dir, 'result')
    process_images_in_folder(folderIn_path, folder_save_folder, inferencer)
    shutil.rmtree(folderIn_path)
