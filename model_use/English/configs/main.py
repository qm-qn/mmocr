import argparse
from Strokes import strokes
from Blank import blank
from Recog import recog
from tqdm import tqdm
import os
import shutil


def count_images_in_folder(folder_path):
    image_count = 0
    for filename in os.listdir(folder_path):
        fileInpath = os.path.join(folder_path, filename)
        if os.path.isdir(fileInpath):
            image_count += count_images_in_folder(fileInpath)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            image_count += 1
    return image_count


def process_images_in_folder(folderIn_path, folder_stroke, folder_blank, folder_result, progress_bar):
    if not os.path.exists(folder_stroke):
        os.makedirs(folder_stroke)
    if not os.path.exists(folder_blank):
        os.makedirs(folder_blank)
    if not os.path.exists(folder_result):
        os.makedirs(folder_result)
    for filename in os.listdir(folderIn_path):
        new_fileInpath = os.path.join(folderIn_path, filename)
        if os.path.isdir(new_fileInpath):
            new_folder_stroke = os.path.join(folder_stroke, filename)
            new_folder_blank = os.path.join(folder_blank, filename)
            new_folder_result = os.path.join(folder_result, filename)
            process_images_in_folder(new_fileInpath, new_folder_stroke, new_folder_blank, new_folder_result, progress_bar)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            process(folderIn_path, folder_stroke, folder_blank, folder_result, progress_bar)
            break


def process(folderIn_path, folder_stroke, folder_blank, folder_result, progress_bar):
    data_list = strokes(folderIn_path, folder_stroke)
    data_list = blank(folder_stroke, folder_blank, data_list, progress_bar)
    recog(folder_blank, folder_result, data_list)


parser = argparse.ArgumentParser(description='Recognization')
parser.add_argument('input_folder', type=str, help='The path to the image')
parser.add_argument('output_folder', type=str, help='The path to the result')
args = parser.parse_args()

progress_bar = tqdm(total=count_images_in_folder(args.input_folder), desc='Processing')
stroke_path = os.path.join(args.output_folder, 'stroke')
blank_path = os.path.join(args.output_folder, 'blank')
result_path = os.path.join(args.output_folder, 'result')
process_images_in_folder(args.input_folder, stroke_path, blank_path, result_path, progress_bar)
shutil.rmtree(stroke_path)
shutil.rmtree(blank_path)
progress_bar.close()
