from mmocr.apis import TextRecInferencer
import os


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


model_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster_IAM_ocren2100_TAL_OCR_ENG_maxepochs288_Tmax8_etamin4e-6_lr4e-4/20240321_002725/vis_data/config.py'
weight_path = '/public/yuziyang/work_dirs/rec/new_dict/lines/aster_IAM_ocren2100_TAL_OCR_ENG_maxepochs288_Tmax8_etamin4e-6_lr4e-4/epoch_288.pth'
# 读取模型
inferencer = TextRecInferencer(model=model_path, weights=weight_path, device='cuda:0')

input_path = 'm_testout/testin'
output_path = 'm_testout/testout'
if not os.path.exists(output_path):
    os.makedirs(output_path)
innermost_folders = find_innermost_folders(input_path)
if innermost_folders:
    for folder in innermost_folders:
        # 推理
        inferencer(folder, out_dir=output_path, save_pred=True, save_vis=True)
else:
    print("该文件夹为空或只包含子文件夹。")
